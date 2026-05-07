const presets = [
  { id: '16:9', name: '9:16', width: 720, height: 1280 },
  { id: '4:3', name: '3:4', width: 900, height: 1200 },
];

const palette = ['#0f172a', '#1d4ed8', '#7c3aed', '#ea580c', '#059669', '#be123c'];
const SNAP_MESSAGE_DEFAULT = '吸附辅助已开启：靠近边缘、中心或铺满/完整显示时会自动贴合。';
const SNAP_MESSAGE_DURATION = 1200;

const state = {
  images: [],
  presetId: presets[0].id,
  templateId: null,
  background: '#111827',
  splitLine: {
    enabled: true,
    color: '#ff4d73',
    width: 2,
  },
  selectedSlotId: null,
  placements: {},
  ui: {
    snapMessage: SNAP_MESSAGE_DEFAULT,
    snapActive: false,
    snapGuides: null,
    snapTimer: null,
  },
  pointerState: {
    pointers: new Map(),
    drag: null,
    pinch: null,
  },
  exportState: {
    busy: false,
    message: '',
    tone: '',
    fallbackUrl: '',
    fallbackFilename: '',
  },
};

let imageIdSeed = 1;
const objectUrls = new Set();

const canvas = document.getElementById('editorCanvas');
const ctx = canvas.getContext('2d');
const canvasWrap = document.getElementById('canvasWrap');
const fileInput = document.getElementById('fileInput');
const dropzone = document.getElementById('dropzone');
const imageListEl = document.getElementById('imageList');
const presetGroupEl = document.getElementById('presetGroup');
const templateGroupsEl = document.getElementById('templateGroups');
const backgroundColorEl = document.getElementById('backgroundColor');
const exportScaleSelectEl = document.getElementById('exportScaleSelect');
const rotationRangeEl = document.getElementById('rotationRange');
const rotationValueEl = document.getElementById('rotationValue');
const scaleRangeEl = document.getElementById('scaleRange');
const scaleValueEl = document.getElementById('scaleValue');
const slotImageSelectEl = document.getElementById('slotImageSelect');
const selectedSlotBadgeEl = document.getElementById('selectedSlotBadge');
const selectedSlotMetaEl = document.getElementById('selectedSlotMeta');
const stageMetaEl = document.getElementById('stageMeta');
const snapHintEl = document.getElementById('snapHint');
const exportPngBtn = document.getElementById('exportPngBtn');
const exportJpgBtn = document.getElementById('exportJpgBtn');
const resetProjectBtn = document.getElementById('resetProjectBtn');
const fitImageBtn = document.getElementById('fitImageBtn');
const containImageBtn = document.getElementById('containImageBtn');
const resetSlotBtn = document.getElementById('resetSlotBtn');
const exportHintEl = document.getElementById('exportHint');
const exportFallbackEl = document.getElementById('exportFallback');
const exportFallbackLinkEl = document.getElementById('exportFallbackLink');
const splitLineColorEl = document.getElementById('splitLineColor');
const splitLineWidthEl = document.getElementById('splitLineWidth');
const splitLineWidthValueEl = document.getElementById('splitLineWidthValue');
const splitLineToggleEl = document.getElementById('splitLineToggle');

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function degToRad(deg) {
  return (deg * Math.PI) / 180;
}

function getCurrentPreset() {
  return presets.find((preset) => preset.id === state.presetId) || presets[0];
}

function rect(x, y, width, height) {
  return {
    type: 'rect',
    x,
    y,
    width,
    height,
  };
}

function rectToPolygon(shape) {
  return [
    { x: shape.x, y: shape.y },
    { x: shape.x + shape.width, y: shape.y },
    { x: shape.x + shape.width, y: shape.y + shape.height },
    { x: shape.x, y: shape.y + shape.height },
  ];
}

function shapeToPolygon(shape) {
  return shape.type === 'rect' ? rectToPolygon(shape) : shape.points;
}

function scalePolygon(points, width, height) {
  return points.map((point) => ({ x: point.x * width, y: point.y * height }));
}

function getPolygonBounds(points) {
  const xs = points.map((point) => point.x);
  const ys = points.map((point) => point.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  return {
    minX,
    maxX,
    minY,
    maxY,
    width: maxX - minX,
    height: maxY - minY,
    centerX: (minX + maxX) / 2,
    centerY: (minY + maxY) / 2,
  };
}

function pointInPolygon(point, polygon) {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const xi = polygon[i].x;
    const yi = polygon[i].y;
    const xj = polygon[j].x;
    const yj = polygon[j].y;
    const intersect = yi > point.y !== yj > point.y && point.x < ((xj - xi) * (point.y - yi)) / (yj - yi || 1e-6) + xi;
    if (intersect) inside = !inside;
  }
  return inside;
}

function getPerimeterPosition(point) {
  const epsilon = 1e-5;
  if (Math.abs(point.y) < epsilon) return point.x;
  if (Math.abs(point.x - 1) < epsilon) return 1 + point.y;
  if (Math.abs(point.y - 1) < epsilon) return 2 + (1 - point.x);
  return 3 + (1 - point.y);
}

function getRayIntersection(cx, cy, angleDeg) {
  const rad = degToRad(angleDeg);
  const dx = Math.cos(rad);
  const dy = Math.sin(rad);
  const candidates = [];

  if (Math.abs(dx) > 1e-6) {
    const tLeft = (0 - cx) / dx;
    const yLeft = cy + tLeft * dy;
    if (tLeft > 0 && yLeft >= 0 && yLeft <= 1) candidates.push({ x: 0, y: yLeft });

    const tRight = (1 - cx) / dx;
    const yRight = cy + tRight * dy;
    if (tRight > 0 && yRight >= 0 && yRight <= 1) candidates.push({ x: 1, y: yRight });
  }

  if (Math.abs(dy) > 1e-6) {
    const tTop = (0 - cy) / dy;
    const xTop = cx + tTop * dx;
    if (tTop > 0 && xTop >= 0 && xTop <= 1) candidates.push({ x: xTop, y: 0 });

    const tBottom = (1 - cy) / dy;
    const xBottom = cx + tBottom * dx;
    if (tBottom > 0 && xBottom >= 0 && xBottom <= 1) candidates.push({ x: xBottom, y: 1 });
  }

  if (!candidates.length) return { x: clamp(cx + dx, 0, 1), y: clamp(cy + dy, 0, 1) };

  candidates.sort((a, b) => {
    const da = (a.x - cx) ** 2 + (a.y - cy) ** 2;
    const db = (b.x - cx) ** 2 + (b.y - cy) ** 2;
    return da - db;
  });

  return candidates[0];
}

function getCornersBetween(startS, endS) {
  const corners = [
    { s: 1, point: { x: 1, y: 0 } },
    { s: 2, point: { x: 1, y: 1 } },
    { s: 3, point: { x: 0, y: 1 } },
    { s: 4, point: { x: 0, y: 0 } },
  ];

  let adjustedEnd = endS;
  if (adjustedEnd <= startS) adjustedEnd += 4;

  return corners
    .map((corner) => ({
      ...corner,
      checkS: corner.s <= startS ? corner.s + 4 : corner.s,
    }))
    .filter((corner) => corner.checkS > startS && corner.checkS < adjustedEnd)
    .map((corner) => corner.point);
}

function createTemplateFromBoundary({ id, name, count, center, boundary }) {
  const sortedBoundary = [...boundary].sort((a, b) => a.perimeter - b.perimeter)

  const slots = sortedBoundary.map((item, index) => {
    const next = sortedBoundary[(index + 1) % sortedBoundary.length]
    const points = [
      { x: center.x, y: center.y },
      item.point,
      ...getCornersBetween(item.perimeter, next.perimeter),
      next.point,
    ]

    return {
      id: `${id}-slot-${index + 1}`,
      shape: { type: 'polygon', points },
    }
  })

  return {
    id,
    name,
    category: 'radial-diagonal',
    supportedCounts: [count],
    aspectRatios: presets.map((preset) => preset.id),
    slots,
  }
}

function createOddRadialTemplate({ id, name, count, angles, center = { x: 0.5, y: 0.5 } }) {
  const boundary = angles.map((angle, index) => {
    const point = getRayIntersection(center.x, center.y, angle)
    return {
      id: `${id}-ray-${index + 1}`,
      angle,
      point,
      perimeter: getPerimeterPosition(point),
    }
  })

  return createTemplateFromBoundary({ id, name, count, center, boundary })
}

function createBoundaryTemplate({ id, name, count, points, center = { x: 0.5, y: 0.5 } }) {
  const boundary = points.map((point, index) => ({
    id: `${id}-point-${index + 1}`,
    point,
    perimeter: getPerimeterPosition(point),
  }))

  return createTemplateFromBoundary({ id, name, count, center, boundary })
}

function createDirectPolygonTemplate({ id, name, count, polygons }) {
  return {
    id,
    name,
    category: 'radial-diagonal',
    supportedCounts: [count],
    aspectRatios: presets.map((preset) => preset.id),
    slots: polygons.map((points, index) => ({
      id: `${id}-slot-${index + 1}`,
      shape: { type: 'polygon', points },
    })),
  }
}

function createEvenCrossTemplate({ id, name, count, lineAngles, boundaryPoints, center = { x: 0.5, y: 0.5 } }) {
  const boundary = boundaryPoints
    ? boundaryPoints.map((point, index) => ({
        id: `${id}-boundary-${index + 1}`,
        point,
        perimeter: getPerimeterPosition(point),
      }))
    : lineAngles.flatMap((angle, index) => {
        const pointA = getRayIntersection(center.x, center.y, angle)
        const pointB = getRayIntersection(center.x, center.y, angle + 180)
        return [
          {
            id: `${id}-line-${index + 1}-a`,
            angle,
            point: pointA,
            perimeter: getPerimeterPosition(pointA),
          },
          {
            id: `${id}-line-${index + 1}-b`,
            angle: angle + 180,
            point: pointB,
            perimeter: getPerimeterPosition(pointB),
          },
        ]
      })

  return createTemplateFromBoundary({ id, name, count, center, boundary })
}

function createEqualColumnsTemplate(count) {
  return {
    id: `columns-${count}`,
    name: `${count}图横向等分`,
    category: 'regular',
    supportedCounts: [count],
    aspectRatios: presets.map((preset) => preset.id),
    slots: Array.from({ length: count }, (_, index) => ({
      id: `columns-${count}-slot-${index + 1}`,
      shape: rect(index / count, 0, 1 / count, 1),
    })),
  };
}

function createEqualRowsTemplate(count) {
  return {
    id: `rows-${count}`,
    name: `${count}图竖向等分`,
    category: 'regular',
    supportedCounts: [count],
    aspectRatios: presets.map((preset) => preset.id),
    slots: Array.from({ length: count }, (_, index) => ({
      id: `rows-${count}-slot-${index + 1}`,
      shape: rect(0, index / count, 1, 1 / count),
    })),
  };
}

function createGridTemplate(count) {
  const cols = Math.ceil(Math.sqrt(count));
  const rows = Math.ceil(count / cols);
  const slots = [];
  for (let index = 0; index < count; index += 1) {
    const row = Math.floor(index / cols);
    const col = index % cols;
    const width = 1 / cols;
    const height = 1 / rows;
    slots.push({
      id: `grid-${count}-slot-${index + 1}`,
      shape: rect(col * width, row * height, width, height),
    });
  }

  return {
    id: `grid-${count}`,
    name: `${count}图网格`,
    category: 'regular',
    supportedCounts: [count],
    aspectRatios: presets.map((preset) => preset.id),
    slots,
  };
}

function createHeroTemplate(count) {
  const slots = [{ id: `hero-${count}-slot-1`, shape: rect(0, 0, 0.56, 1) }];
  const rest = count - 1;
  for (let index = 0; index < rest; index += 1) {
    slots.push({
      id: `hero-${count}-slot-${index + 2}`,
      shape: rect(0.56, index / rest, 0.44, 1 / rest),
    });
  }

  return {
    id: `hero-${count}`,
    name: `${count}图主次分屏`,
    category: 'regular',
    supportedCounts: [count],
    aspectRatios: presets.map((preset) => preset.id),
    slots,
  };
}

const diagonalTemplateRules = window.DIAGONAL_TEMPLATE_RULES || []

function buildDiagonalTemplate(rule) {
  if (rule.mode === 'explicit') {
    return createDirectPolygonTemplate({
      id: rule.id,
      name: rule.name,
      count: rule.count,
      polygons: rule.polygons,
    })
  }

  if (rule.mode === 'odd-radial') {
    return createOddRadialTemplate({
      id: rule.id,
      name: rule.name,
      count: rule.count,
      center: rule.center,
      angles: rule.angles,
    })
  }

  return createEvenCrossTemplate({
    id: rule.id,
    name: rule.name,
    count: rule.count,
    center: rule.center,
    boundaryPoints: rule.boundaryPoints,
  })
}

const templates = [
  createEqualColumnsTemplate(2),
  createEqualRowsTemplate(2),
  createEqualColumnsTemplate(3),
  createEqualRowsTemplate(3),
  createHeroTemplate(3),
  createGridTemplate(4),
  createHeroTemplate(4),
  createGridTemplate(5),
  createHeroTemplate(5),
  createGridTemplate(6),
  createHeroTemplate(6),
  createGridTemplate(7),
  createGridTemplate(8),
  createGridTemplate(9),
  createGridTemplate(10),
  createGridTemplate(11),
  createGridTemplate(12),
  ...diagonalTemplateRules.map(buildDiagonalTemplate),
];

function getFilteredTemplates() {
  const count = state.images.length;
  const currentPreset = getCurrentPreset();
  return templates.filter((template) => {
    const countMatch = count === 0 ? true : template.supportedCounts.includes(count);
    const aspectMatch = template.aspectRatios.includes(currentPreset.id);
    return countMatch && aspectMatch;
  });
}

function getCurrentTemplate() {
  return templates.find((template) => template.id === state.templateId) || null;
}

function getSlotById(slotId) {
  const template = getCurrentTemplate();
  return template?.slots.find((slot) => slot.id === slotId) || null;
}

function getImageById(imageId) {
  return state.images.find((image) => image.id === imageId) || null;
}

function defaultPlacement(slot, imageId = null) {
  return {
    slotId: slot.id,
    imageId,
    x: 0,
    y: 0,
    scale: 1,
    rotation: 0,
    fitMode: 'cover',
  };
}

function setSnapFeedback(message = SNAP_MESSAGE_DEFAULT, guides = null, active = false) {
  state.ui.snapMessage = message;
  state.ui.snapActive = active;
  state.ui.snapGuides = guides;

  if (state.ui.snapTimer) {
    clearTimeout(state.ui.snapTimer);
    state.ui.snapTimer = null;
  }

  if (active) {
    state.ui.snapTimer = window.setTimeout(() => {
      state.ui.snapMessage = SNAP_MESSAGE_DEFAULT;
      state.ui.snapActive = false;
      state.ui.snapGuides = null;
      renderCanvas();
    }, SNAP_MESSAGE_DURATION);
  }
}

function clearSnapFeedback() {
  setSnapFeedback(SNAP_MESSAGE_DEFAULT, null, false);
}

function ensureTemplateSelection() {
  const filtered = getFilteredTemplates();
  if (!filtered.length) {
    state.templateId = null;
    state.selectedSlotId = null;
    state.placements = {};
    return;
  }

  const hasCurrent = filtered.some((template) => template.id === state.templateId);
  if (!hasCurrent) state.templateId = filtered[0].id;

  syncPlacementsForTemplate();
}

function syncPlacementsForTemplate() {
  const template = getCurrentTemplate();
  if (!template) {
    state.placements = {};
    return;
  }

  const previousPlacements = state.placements;
  const nextPlacements = {};
  const usedImageIds = new Set();

  template.slots.forEach((slot) => {
    const previous = previousPlacements[slot.id];
    if (previous && state.images.some((image) => image.id === previous.imageId)) {
      nextPlacements[slot.id] = { ...previous };
      if (previous.imageId) usedImageIds.add(previous.imageId);
      return;
    }

    const availableImage = state.images.find((image) => !usedImageIds.has(image.id));
    const placement = defaultPlacement(slot, availableImage?.id || null);
    nextPlacements[slot.id] = placement;
    if (placement.imageId) usedImageIds.add(placement.imageId);
  });

  state.placements = nextPlacements;
  if (!state.selectedSlotId || !template.slots.some((slot) => slot.id === state.selectedSlotId)) {
    state.selectedSlotId = template.slots[0]?.id || null;
  }
}

function getCanvasPoint(event) {
  const rectEl = canvas.getBoundingClientRect();
  return {
    x: ((event.clientX - rectEl.left) / rectEl.width) * canvas.width,
    y: ((event.clientY - rectEl.top) / rectEl.height) * canvas.height,
  };
}

function getBaseScalePair(image, bounds) {
  if (!image) return { cover: 1, contain: 1 };
  return {
    cover: Math.max(bounds.width / image.width, bounds.height / image.height),
    contain: Math.min(bounds.width / image.width, bounds.height / image.height),
  };
}

function getBaseScale(image, bounds, fitMode) {
  const pair = getBaseScalePair(image, bounds);
  return fitMode === 'contain' ? pair.contain : pair.cover;
}

function getPlacementMetrics(slot, placement, width, height) {
  const polygon = scalePolygon(shapeToPolygon(slot.shape), width, height);
  const bounds = getPolygonBounds(polygon);
  const image = placement?.imageId ? getImageById(placement.imageId) : null;
  const scalePair = getBaseScalePair(image, bounds);
  const baseScale = placement ? getBaseScale(image, bounds, placement.fitMode) : 1;
  const finalScale = placement ? baseScale * placement.scale : 1;
  const centerX = bounds.centerX + (placement?.x || 0) * width;
  const centerY = bounds.centerY + (placement?.y || 0) * height;
  const renderWidth = image ? image.width * finalScale : 0;
  const renderHeight = image ? image.height * finalScale : 0;

  return {
    polygon,
    bounds,
    image,
    scalePair,
    baseScale,
    finalScale,
    centerX,
    centerY,
    renderWidth,
    renderHeight,
    left: centerX - renderWidth / 2,
    right: centerX + renderWidth / 2,
    top: centerY - renderHeight / 2,
    bottom: centerY + renderHeight / 2,
  };
}

function fitPlacementToSlot(slotId, fitMode = 'cover') {
  const placement = state.placements[slotId];
  if (!placement) return;
  placement.x = 0;
  placement.y = 0;
  placement.rotation = 0;
  placement.scale = 1;
  placement.fitMode = fitMode;
  setSnapFeedback(fitMode === 'cover' ? '已铺满当前区域' : '已切换为完整显示', null, true);
}

function getPreviewRatioCss() {
  const preset = getCurrentPreset();
  return `${preset.width} / ${preset.height}`;
}

function updatePreviewRatio() {
  canvasWrap.style.setProperty('--canvas-ratio', getPreviewRatioCss());
}

function applyScaleSnap(slot, placement, proposedScale) {
  const metrics = getPlacementMetrics(slot, placement, canvas.width, canvas.height);
  if (!metrics.image) return { scale: clamp(proposedScale, 0.5, 2.5), fitMode: placement.fitMode, feedback: null };

  const rawScale = getBaseScale(metrics.image, metrics.bounds, placement.fitMode) * proposedScale;
  const coverDistance = Math.abs(rawScale - metrics.scalePair.cover) / metrics.scalePair.cover;
  const containDistance = Math.abs(rawScale - metrics.scalePair.contain) / metrics.scalePair.contain;
  const snapThreshold = 0.045;

  if (coverDistance <= snapThreshold) {
    return {
      scale: 1,
      fitMode: 'cover',
      feedback: { message: '已吸附到铺满当前区域', guides: null },
    };
  }

  if (containDistance <= snapThreshold) {
    return {
      scale: 1,
      fitMode: 'contain',
      feedback: { message: '已吸附到完整显示', guides: null },
    };
  }

  return { scale: clamp(proposedScale, 0.5, 2.5), fitMode: placement.fitMode, feedback: null };
}

function applyPositionSnap(slot, placement, proposedX, proposedY) {
  const metrics = getPlacementMetrics(
    slot,
    {
      ...placement,
      x: proposedX,
      y: proposedY,
    },
    canvas.width,
    canvas.height
  );

  if (!metrics.image || Math.abs(placement.rotation) > 2) {
    return {
      x: proposedX,
      y: proposedY,
      feedback: null,
    };
  }

  const threshold = Math.max(10, Math.min(canvas.width, canvas.height) * 0.02);
  let snappedX = proposedX;
  let snappedY = proposedY;
  let guideX = null;
  let guideY = null;
  const labels = [];

  const xCandidates = [
    {
      label: '左边缘',
      targetX: (metrics.bounds.minX + metrics.renderWidth / 2 - metrics.bounds.centerX) / canvas.width,
      guide: metrics.bounds.minX,
      diff: Math.abs(metrics.left - metrics.bounds.minX),
    },
    {
      label: '水平居中',
      targetX: 0,
      guide: metrics.bounds.centerX,
      diff: Math.abs(metrics.centerX - metrics.bounds.centerX),
    },
    {
      label: '右边缘',
      targetX: (metrics.bounds.maxX - metrics.renderWidth / 2 - metrics.bounds.centerX) / canvas.width,
      guide: metrics.bounds.maxX,
      diff: Math.abs(metrics.right - metrics.bounds.maxX),
    },
  ].sort((a, b) => a.diff - b.diff);

  if (xCandidates[0].diff <= threshold) {
    snappedX = xCandidates[0].targetX;
    guideX = xCandidates[0].guide;
    labels.push(xCandidates[0].label);
  }

  const yCandidates = [
    {
      label: '上边缘',
      targetY: (metrics.bounds.minY + metrics.renderHeight / 2 - metrics.bounds.centerY) / canvas.height,
      guide: metrics.bounds.minY,
      diff: Math.abs(metrics.top - metrics.bounds.minY),
    },
    {
      label: '垂直居中',
      targetY: 0,
      guide: metrics.bounds.centerY,
      diff: Math.abs(metrics.centerY - metrics.bounds.centerY),
    },
    {
      label: '下边缘',
      targetY: (metrics.bounds.maxY - metrics.renderHeight / 2 - metrics.bounds.centerY) / canvas.height,
      guide: metrics.bounds.maxY,
      diff: Math.abs(metrics.bottom - metrics.bounds.maxY),
    },
  ].sort((a, b) => a.diff - b.diff);

  if (yCandidates[0].diff <= threshold) {
    snappedY = yCandidates[0].targetY;
    guideY = yCandidates[0].guide;
    labels.push(yCandidates[0].label);
  }

  return {
    x: snappedX,
    y: snappedY,
    feedback: labels.length
      ? {
          message: `已吸附：${labels.join(' / ')}`,
          guides: { x: guideX, y: guideY },
        }
      : null,
  };
}

function drawGuides(ctx2d, guides, width, height) {
  if (!guides) return;

  ctx2d.save();
  ctx2d.setLineDash([10, 8]);
  ctx2d.lineWidth = Math.max(1.5, width * 0.0025);
  ctx2d.strokeStyle = 'rgba(251, 113, 133, 0.9)';

  if (typeof guides.x === 'number') {
    ctx2d.beginPath();
    ctx2d.moveTo(guides.x, 0);
    ctx2d.lineTo(guides.x, height);
    ctx2d.stroke();
  }

  if (typeof guides.y === 'number') {
    ctx2d.beginPath();
    ctx2d.moveTo(0, guides.y);
    ctx2d.lineTo(width, guides.y);
    ctx2d.stroke();
  }

  ctx2d.restore();
}

function drawSlot(ctx2d, slot, placement, width, height, options = {}) {
  const metrics = getPlacementMetrics(slot, placement, width, height);
  const isSelected = options.selectedSlotId === slot.id;

  ctx2d.save();
  ctx2d.beginPath();
  metrics.polygon.forEach((point, index) => {
    if (index === 0) ctx2d.moveTo(point.x, point.y);
    else ctx2d.lineTo(point.x, point.y);
  });
  ctx2d.closePath();
  ctx2d.clip();

  if (metrics.image) {
    ctx2d.save();
    ctx2d.translate(metrics.centerX, metrics.centerY);
    ctx2d.rotate(degToRad(placement.rotation));
    ctx2d.scale(metrics.finalScale, metrics.finalScale);
    ctx2d.drawImage(metrics.image.element, -metrics.image.width / 2, -metrics.image.height / 2, metrics.image.width, metrics.image.height);
    ctx2d.restore();
  } else {
    ctx2d.fillStyle = 'rgba(255,255,255,0.08)';
    ctx2d.fillRect(metrics.bounds.minX, metrics.bounds.minY, metrics.bounds.width, metrics.bounds.height);
    ctx2d.fillStyle = 'rgba(255,255,255,0.66)';
    ctx2d.font = `${Math.max(12, width * 0.018)}px sans-serif`;
    ctx2d.textAlign = 'center';
    ctx2d.textBaseline = 'middle';
    ctx2d.fillText('选择图片', metrics.bounds.centerX, metrics.bounds.centerY);
  }
  ctx2d.restore();

  const shouldDrawBoundary = options.forceShowLines || isSelected || state.splitLine.enabled;
  if (shouldDrawBoundary) {
    ctx2d.save();
    ctx2d.beginPath();
    metrics.polygon.forEach((point, index) => {
      if (index === 0) ctx2d.moveTo(point.x, point.y);
      else ctx2d.lineTo(point.x, point.y);
    });
    ctx2d.closePath();
    ctx2d.strokeStyle = isSelected ? 'rgba(244,63,94,0.95)' : state.splitLine.color;
    const baseLineWidth = Math.max(state.splitLine.width * (width / 720), width * 0.0014);
    ctx2d.lineWidth = isSelected ? Math.max(baseLineWidth + 1, width * 0.0032) : baseLineWidth;
    ctx2d.stroke();
    ctx2d.restore();
  }
}

function renderToContext(ctx2d, width, height, options = {}) {
  const template = getCurrentTemplate();
  ctx2d.clearRect(0, 0, width, height);
  ctx2d.fillStyle = state.background;
  ctx2d.fillRect(0, 0, width, height);

  if (!template) {
    ctx2d.fillStyle = 'rgba(255,255,255,0.15)';
    ctx2d.fillRect(width * 0.08, height * 0.08, width * 0.84, height * 0.84);
    ctx2d.fillStyle = 'rgba(255,255,255,0.75)';
    ctx2d.textAlign = 'center';
    ctx2d.textBaseline = 'middle';
    ctx2d.font = `${Math.max(20, width * 0.03)}px sans-serif`;
    ctx2d.fillText('上传图片后开始拼图', width / 2, height / 2);
    return;
  }

  template.slots.forEach((slot) => {
    drawSlot(ctx2d, slot, state.placements[slot.id], width, height, options);
  });

  if (options.selectedSlotId && options.snapGuides) {
    drawGuides(ctx2d, options.snapGuides, width, height);
  }
}

function resizeCanvasToPreset() {
  const preset = getCurrentPreset();
  canvas.width = preset.width;
  canvas.height = preset.height;
  updatePreviewRatio();
}

function updateSnapHint() {
  snapHintEl.textContent = state.ui.snapMessage;
  snapHintEl.classList.toggle('is-active', state.ui.snapActive);
}

function updateLineStyleControls() {
  splitLineColorEl.value = state.splitLine.color
  splitLineWidthEl.value = String(state.splitLine.width)
  splitLineWidthValueEl.textContent = `${state.splitLine.width}px`
  splitLineToggleEl.checked = state.splitLine.enabled
}

function setExportButtonsLoading(isLoading, label = '') {
  [
    { button: exportPngBtn, idle: '导出 PNG', busy: label || '导出中...' },
    { button: exportJpgBtn, idle: '导出 JPG', busy: label || '导出中...' },
  ].forEach(({ button, idle, busy }) => {
    button.classList.toggle('is-loading', isLoading)
    button.disabled = isLoading
    button.textContent = isLoading ? busy : idle
  })
}

function setExportFeedback(message = '', tone = '', fallbackUrl = '', fallbackFilename = '') {
  state.exportState.message = message
  state.exportState.tone = tone
  state.exportState.fallbackUrl = fallbackUrl
  state.exportState.fallbackFilename = fallbackFilename

  exportHintEl.textContent = message
  exportHintEl.classList.toggle('is-success', tone === 'success')
  exportHintEl.classList.toggle('is-error', tone === 'error')

  if (fallbackUrl) {
    exportFallbackEl.hidden = false
    exportFallbackLinkEl.href = fallbackUrl
    exportFallbackLinkEl.download = fallbackFilename || ''
  } else {
    exportFallbackEl.hidden = true
    exportFallbackLinkEl.href = '#'
    exportFallbackLinkEl.removeAttribute('download')
  }
}

function renderCanvas() {
  resizeCanvasToPreset();
  renderToContext(ctx, canvas.width, canvas.height, {
    selectedSlotId: state.selectedSlotId,
    snapGuides: state.ui.snapGuides,
  });
  renderImageList();
  renderPresetChips();
  renderTemplateCards();
  updateSelectedControls();
  updateStageMeta();
  updateSnapHint();
  updateLineStyleControls();
}

function updateStageMeta() {
  const template = getCurrentTemplate();
  const preset = getCurrentPreset();
  const count = state.images.length;
  const templateName = template ? template.name : '未选择模板';
  stageMetaEl.textContent = `${preset.name}（${preset.width} × ${preset.height}） · ${templateName} · 已上传 ${count} 张图`;
}

function updateSelectedControls() {
  const slot = getSlotById(state.selectedSlotId);
  const placement = slot ? state.placements[slot.id] : null;
  const image = placement?.imageId ? getImageById(placement.imageId) : null;

  if (!slot || !placement) {
    selectedSlotBadgeEl.textContent = '未选中';
    selectedSlotMetaEl.textContent = '选择一个区域后可调整。';
    rotationRangeEl.value = '0';
    rotationValueEl.textContent = '0°';
    scaleRangeEl.value = '100';
    scaleValueEl.textContent = '100%';
    slotImageSelectEl.innerHTML = '<option value="">请先上传图片</option>';
    return;
  }

  const template = getCurrentTemplate();
  const slotIndex = template.slots.findIndex((item) => item.id === slot.id) + 1;
  selectedSlotBadgeEl.textContent = `区域 ${slotIndex}`;
  selectedSlotMetaEl.textContent = image
    ? `当前图片：${image.name}`
    : '当前区域还没有图片，点击左侧缩略图即可指定。';
  rotationRangeEl.value = String(Math.round(placement.rotation));
  rotationValueEl.textContent = `${Math.round(placement.rotation)}°`;
  scaleRangeEl.value = String(Math.round(placement.scale * 100));
  scaleValueEl.textContent = `${Math.round(placement.scale * 100)}%`;

  const options = ['<option value="">不放图片</option>']
    .concat(
      state.images.map(
        (item, index) =>
          `<option value="${item.id}" ${item.id === placement.imageId ? 'selected' : ''}>${index + 1}. ${item.name}</option>`
      )
    )
    .join('');
  slotImageSelectEl.innerHTML = options;
}

function renderPresetChips() {
  presetGroupEl.innerHTML = presets
    .map(
      (preset) => `
        <button class="preset-chip ${preset.id === state.presetId ? 'active' : ''}" data-preset-id="${preset.id}">
          <strong>${preset.name}</strong>
          <p>${preset.width} × ${preset.height}</p>
        </button>
      `
    )
    .join('');
}

function buildTemplatePreview(template) {
  const preset = getCurrentPreset()
  const width = 180
  const height = Math.round((preset.height / preset.width) * width)
  const shapes = template.slots
    .map((slot, index) => {
      const polygon = scalePolygon(shapeToPolygon(slot.shape), width, height)
      const points = polygon.map((point) => `${point.x},${point.y}`).join(' ')
      const stroke = state.splitLine.enabled ? state.splitLine.color : 'transparent'
      const strokeWidth = state.splitLine.enabled ? Math.max(1, state.splitLine.width * 0.75) : 0
      return `<polygon points="${points}" fill="${palette[index % palette.length]}" fill-opacity="0.32" stroke="${stroke}" stroke-width="${strokeWidth}" />`
    })
    .join('')

  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
      <rect width="100%" height="100%" rx="18" fill="#0f172a" />
      ${shapes}
    </svg>
  `

  return {
    backgroundImage: `url(data:image/svg+xml;utf8,${encodeURIComponent(svg)})`,
    aspectRatio: `${preset.width} / ${preset.height}`,
  }
}

function renderTemplateCards() {
  const filtered = getFilteredTemplates();
  const groups = [
    { id: 'regular', title: '基础拼图' },
    { id: 'radial-diagonal', title: '创意斜切' },
  ];

  templateGroupsEl.innerHTML = groups
    .map((group) => {
      const groupTemplates = filtered.filter((template) => template.category === group.id);
      if (!groupTemplates.length) return '';
      return `
        <div>
          <div class="template-group-title">${group.title}</div>
          <div class="template-group-list">
            ${groupTemplates
              .map((template) => {
                const preview = buildTemplatePreview(template)
                return `
                  <button class="template-card ${template.id === state.templateId ? 'active' : ''}" data-template-id="${template.id}">
                    <div class="template-preview" style="--preview-ratio:${preview.aspectRatio}; background-image:${preview.backgroundImage}"></div>
                    <h3>${template.name}</h3>
                    <p>${template.supportedCounts[0]} 张图</p>
                  </button>
                `
              })
              .join('')}
          </div>
        </div>
      `;
    })
    .join('');
}

function renderImageList() {
  if (!state.images.length) {
    imageListEl.innerHTML = '<div class="dropzone"><p>还没有图片</p><span>上传后会显示缩略图和排序操作</span></div>';
    return;
  }

  imageListEl.innerHTML = state.images
    .map((image, index) => {
      const usedInSelectedSlot = state.selectedSlotId && state.placements[state.selectedSlotId]?.imageId === image.id;
      return `
        <div class="image-card ${usedInSelectedSlot ? 'active' : ''}">
          <img src="${image.url}" alt="${image.name}" />
          <div>
            <h3>${index + 1}. ${image.name}</h3>
            <p>${image.width} × ${image.height}</p>
            <div class="image-actions">
              <button class="icon-btn" data-assign-image-id="${image.id}">放入当前区域</button>
              <button class="icon-btn" data-move-image-id="${image.id}" data-direction="up">上移</button>
              <button class="icon-btn" data-move-image-id="${image.id}" data-direction="down">下移</button>
              <button class="icon-btn" data-remove-image-id="${image.id}">删除</button>
            </div>
          </div>
        </div>
      `;
    })
    .join('');
}

async function loadFiles(fileList) {
  const files = Array.from(fileList || []).filter((file) => file.type.startsWith('image/'));
  if (!files.length) return;

  const room = 12 - state.images.length;
  const acceptedFiles = files.slice(0, room);
  if (!acceptedFiles.length) {
    alert('最多支持 12 张图片。');
    return;
  }

  const loaded = await Promise.all(
    acceptedFiles.map(
      (file) =>
        new Promise((resolve, reject) => {
          const url = URL.createObjectURL(file);
          objectUrls.add(url);
          const element = new Image();
          element.onload = () =>
            resolve({
              id: `img-${(imageIdSeed += 1)}`,
              name: file.name,
              width: element.naturalWidth,
              height: element.naturalHeight,
              url,
              element,
            });
          element.onerror = reject;
          element.src = url;
        })
    )
  );

  state.images.push(...loaded);
  ensureTemplateSelection();
  renderCanvas();
}

function assignImageToSelectedSlot(imageId) {
  const placement = state.selectedSlotId ? state.placements[state.selectedSlotId] : null;
  if (!placement) return;
  placement.imageId = imageId;
  placement.scale = 1;
  placement.rotation = 0;
  placement.x = 0;
  placement.y = 0;
  placement.fitMode = 'cover';
  clearSnapFeedback();
  renderCanvas();
}

function removeImage(imageId) {
  const index = state.images.findIndex((image) => image.id === imageId);
  if (index === -1) return;
  const [removed] = state.images.splice(index, 1);
  if (removed?.url) {
    URL.revokeObjectURL(removed.url);
    objectUrls.delete(removed.url);
  }

  Object.values(state.placements).forEach((placement) => {
    if (placement.imageId === imageId) placement.imageId = null;
  });

  ensureTemplateSelection();
  clearSnapFeedback();
  renderCanvas();
}

function moveImage(imageId, direction) {
  const index = state.images.findIndex((image) => image.id === imageId);
  if (index === -1) return;
  const nextIndex = direction === 'up' ? index - 1 : index + 1;
  if (nextIndex < 0 || nextIndex >= state.images.length) return;
  const [item] = state.images.splice(index, 1);
  state.images.splice(nextIndex, 0, item);
  syncPlacementsForTemplate();
  renderCanvas();
}

function exportImage(type) {
  if (state.exportState.busy) return

  const preset = getCurrentPreset();
  const scale = Number(exportScaleSelectEl.value || '2');
  const exportCanvas = document.createElement('canvas');
  exportCanvas.width = preset.width * scale;
  exportCanvas.height = preset.height * scale;
  const exportCtx = exportCanvas.getContext('2d');
  renderToContext(exportCtx, exportCanvas.width, exportCanvas.height, {});

  const mimeType = type === 'jpg' ? 'image/jpeg' : 'image/png';
  const quality = type === 'jpg' ? 0.95 : 1;
  const filename = `xhs-collage-${state.presetId.replace(':', '-')}.${type}`;

  state.exportState.busy = true
  setExportButtonsLoading(true, `导出 ${type.toUpperCase()}...`)
  setExportFeedback(`正在生成 ${type.toUpperCase()} 文件...`, '', '', '')

  window.setTimeout(() => {
    try {
      const dataUrl = exportCanvas.toDataURL(mimeType, quality)
      const link = document.createElement('a')
      link.href = dataUrl
      link.download = filename
      link.rel = 'noopener'
      document.body.appendChild(link)
      link.click()
      link.remove()
      setExportFeedback(`已触发 ${type.toUpperCase()} 下载：${filename}`, 'success', '', '')
    } catch (error) {
      console.error('Export failed', error)
      setExportFeedback(`自动下载失败，可手动打开导出结果：${filename}`, 'error', '', filename)
      try {
        const fallbackUrl = exportCanvas.toDataURL(mimeType, quality)
        setExportFeedback(`自动下载失败，可手动打开导出结果：${filename}`, 'error', fallbackUrl, filename)
      } catch (_) {
        // ignore nested failure
      }
    } finally {
      state.exportState.busy = false
      setExportButtonsLoading(false)
    }
  }, 80)
}

function hitTestSlot(point) {
  const template = getCurrentTemplate();
  if (!template) return null;

  for (let index = template.slots.length - 1; index >= 0; index -= 1) {
    const slot = template.slots[index];
    const polygon = scalePolygon(shapeToPolygon(slot.shape), canvas.width, canvas.height);
    if (pointInPolygon(point, polygon)) return slot;
  }
  return null;
}

function updatePointer(event) {
  state.pointerState.pointers.set(event.pointerId, getCanvasPoint(event));
}

function clearPointer(event) {
  state.pointerState.pointers.delete(event.pointerId);
  if (state.pointerState.pointers.size < 2) state.pointerState.pinch = null;
  if (state.pointerState.drag?.pointerId === event.pointerId) state.pointerState.drag = null;
}

function handlePointerDown(event) {
  const point = getCanvasPoint(event);
  updatePointer(event);
  const slot = hitTestSlot(point);
  if (slot) {
    state.selectedSlotId = slot.id;
    const placement = state.placements[slot.id];
    if (placement?.imageId) {
      state.pointerState.drag = {
        pointerId: event.pointerId,
        slotId: slot.id,
        startPoint: point,
        startX: placement.x,
        startY: placement.y,
      };
    }
  }

  if (state.pointerState.pointers.size === 2 && state.selectedSlotId) {
    const [a, b] = [...state.pointerState.pointers.values()];
    const distance = Math.hypot(a.x - b.x, a.y - b.y);
    const placement = state.placements[state.selectedSlotId];
    if (placement) {
      state.pointerState.pinch = {
        startDistance: distance,
        startScale: placement.scale,
      };
      state.pointerState.drag = null;
    }
  }

  clearSnapFeedback();
  renderCanvas();
}

function handlePointerMove(event) {
  if (!state.pointerState.pointers.has(event.pointerId)) return;
  const point = getCanvasPoint(event);
  state.pointerState.pointers.set(event.pointerId, point);

  const slot = getSlotById(state.selectedSlotId);
  const placement = slot ? state.placements[state.selectedSlotId] : null;
  if (!placement || !slot) return;

  if (state.pointerState.pinch && state.pointerState.pointers.size >= 2) {
    const [a, b] = [...state.pointerState.pointers.values()];
    const distance = Math.hypot(a.x - b.x, a.y - b.y);
    const nextScale = clamp((distance / state.pointerState.pinch.startDistance) * state.pointerState.pinch.startScale, 0.5, 2.5);
    const snapped = applyScaleSnap(slot, placement, nextScale);
    placement.scale = snapped.scale;
    placement.fitMode = snapped.fitMode;
    if (snapped.feedback) setSnapFeedback(snapped.feedback.message, snapped.feedback.guides, true);
    else clearSnapFeedback();
    renderCanvas();
    return;
  }

  const drag = state.pointerState.drag;
  if (!drag || drag.pointerId !== event.pointerId || drag.slotId !== state.selectedSlotId) return;

  const proposedX = drag.startX + (point.x - drag.startPoint.x) / canvas.width;
  const proposedY = drag.startY + (point.y - drag.startPoint.y) / canvas.height;
  const snapped = applyPositionSnap(slot, placement, proposedX, proposedY);
  placement.x = snapped.x;
  placement.y = snapped.y;
  if (snapped.feedback) setSnapFeedback(snapped.feedback.message, snapped.feedback.guides, true);
  else clearSnapFeedback();
  renderCanvas();
}

function handlePointerUp(event) {
  clearPointer(event);
  if (!state.pointerState.drag && !state.pointerState.pinch) {
    state.ui.snapGuides = null;
    state.ui.snapActive = false;
    state.ui.snapMessage = SNAP_MESSAGE_DEFAULT;
  }
  renderCanvas();
}

function bindEvents() {
  fileInput.addEventListener('change', (event) => {
    loadFiles(event.target.files);
    fileInput.value = '';
  });

  ['dragenter', 'dragover'].forEach((type) => {
    dropzone.addEventListener(type, (event) => {
      event.preventDefault();
      dropzone.classList.add('is-dragover');
    });
  });

  ['dragleave', 'drop'].forEach((type) => {
    dropzone.addEventListener(type, (event) => {
      event.preventDefault();
      dropzone.classList.remove('is-dragover');
    });
  });

  dropzone.addEventListener('drop', (event) => {
    loadFiles(event.dataTransfer.files);
  });

  document.addEventListener('click', (event) => {
    const presetBtn = event.target.closest('[data-preset-id]');
    if (presetBtn) {
      state.presetId = presetBtn.dataset.presetId;
      ensureTemplateSelection();
      clearSnapFeedback();
      renderCanvas();
      return;
    }

    const templateBtn = event.target.closest('[data-template-id]');
    if (templateBtn) {
      state.templateId = templateBtn.dataset.templateId;
      syncPlacementsForTemplate();
      clearSnapFeedback();
      renderCanvas();
      return;
    }

    const assignBtn = event.target.closest('[data-assign-image-id]');
    if (assignBtn) {
      assignImageToSelectedSlot(assignBtn.dataset.assignImageId);
      return;
    }

    const moveBtn = event.target.closest('[data-move-image-id]');
    if (moveBtn) {
      moveImage(moveBtn.dataset.moveImageId, moveBtn.dataset.direction);
      return;
    }

    const removeBtn = event.target.closest('[data-remove-image-id]');
    if (removeBtn) {
      removeImage(removeBtn.dataset.removeImageId);
    }
  });

  backgroundColorEl.addEventListener('input', (event) => {
    state.background = event.target.value;
    renderCanvas();
  });

  splitLineColorEl.addEventListener('input', (event) => {
    state.splitLine.color = event.target.value;
    renderCanvas();
  });

  splitLineWidthEl.addEventListener('input', (event) => {
    state.splitLine.width = Number(event.target.value);
    renderCanvas();
  });

  splitLineToggleEl.addEventListener('change', (event) => {
    state.splitLine.enabled = event.target.checked;
    renderCanvas();
  });

  rotationRangeEl.addEventListener('input', (event) => {
    const placement = state.selectedSlotId ? state.placements[state.selectedSlotId] : null;
    if (!placement) return;
    placement.rotation = Number(event.target.value);
    clearSnapFeedback();
    renderCanvas();
  });

  scaleRangeEl.addEventListener('input', (event) => {
    const slot = getSlotById(state.selectedSlotId);
    const placement = state.selectedSlotId ? state.placements[state.selectedSlotId] : null;
    if (!placement || !slot) return;
    const snapped = applyScaleSnap(slot, placement, Number(event.target.value) / 100);
    placement.scale = snapped.scale;
    placement.fitMode = snapped.fitMode;
    if (snapped.feedback) setSnapFeedback(snapped.feedback.message, null, true);
    else clearSnapFeedback();
    renderCanvas();
  });

  slotImageSelectEl.addEventListener('change', (event) => {
    const placement = state.selectedSlotId ? state.placements[state.selectedSlotId] : null;
    if (!placement) return;
    placement.imageId = event.target.value || null;
    placement.x = 0;
    placement.y = 0;
    placement.rotation = 0;
    placement.scale = 1;
    placement.fitMode = 'cover';
    clearSnapFeedback();
    renderCanvas();
  });

  exportPngBtn.addEventListener('click', () => exportImage('png'));
  exportJpgBtn.addEventListener('click', () => exportImage('jpg'));

  resetProjectBtn.addEventListener('click', () => {
    state.images.forEach((image) => {
      if (image.url) {
        URL.revokeObjectURL(image.url);
        objectUrls.delete(image.url);
      }
    });
    state.images = [];
    state.templateId = null;
    state.selectedSlotId = null;
    state.placements = {};
    clearSnapFeedback();
    renderCanvas();
  });

  fitImageBtn.addEventListener('click', () => {
    if (!state.selectedSlotId) return;
    fitPlacementToSlot(state.selectedSlotId, 'cover');
    renderCanvas();
  });

  containImageBtn.addEventListener('click', () => {
    if (!state.selectedSlotId) return;
    fitPlacementToSlot(state.selectedSlotId, 'contain');
    renderCanvas();
  });

  resetSlotBtn.addEventListener('click', () => {
    if (!state.selectedSlotId) return;
    fitPlacementToSlot(state.selectedSlotId, 'cover');
    renderCanvas();
  });

  canvas.addEventListener('pointerdown', handlePointerDown);
  canvas.addEventListener('pointermove', handlePointerMove);
  canvas.addEventListener('pointerup', handlePointerUp);
  canvas.addEventListener('pointercancel', handlePointerUp);
  canvas.addEventListener('pointerleave', handlePointerUp);

  canvas.addEventListener(
    'wheel',
    (event) => {
      if (!state.selectedSlotId) return;
      const slot = getSlotById(state.selectedSlotId);
      const placement = state.placements[state.selectedSlotId];
      if (!placement || !slot) return;
      event.preventDefault();
      const rawScale = placement.scale + (event.deltaY > 0 ? -0.05 : 0.05);
      const snapped = applyScaleSnap(slot, placement, rawScale);
      placement.scale = snapped.scale;
      placement.fitMode = snapped.fitMode;
      if (snapped.feedback) setSnapFeedback(snapped.feedback.message, null, true);
      else clearSnapFeedback();
      renderCanvas();
    },
    { passive: false }
  );

  window.addEventListener('beforeunload', () => {
    objectUrls.forEach((url) => URL.revokeObjectURL(url));
  });
}

function init() {
  renderPresetChips();
  updatePreviewRatio();
  ensureTemplateSelection();
  bindEvents();
  renderCanvas();
}

init();
