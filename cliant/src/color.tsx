const backGroundPulsLch = [94, 10, 255] // 評価値先手有利の色
const backGroundEvenLch = [84, 18, 85] // 評価値互角の色
const backGroundNegaLch = [84, 18, 365] // 評価値後手有利の色
// 色は線形に変化させる
const minimumValue = 50 // 変化させる最小の評価値
const maximumValue = 400 // 変化させる最大の評価値
const minimumColor = 5
const maximumColor = 55
const linierColorFunc = (value: number) => {
  if (value <= minimumValue) {
    return minimumColor
  }
  if (value >= maximumValue) {
    return maximumColor
  }
  const v = value - minimumValue
  const a = (maximumColor - minimumColor) / (maximumValue - minimumValue)
  return a * v + minimumColor
}

const getRgb = (value: number) => {
  let base = [0, 0, 0]
  if (value >= minimumValue) {
    base = backGroundPulsLch
    base[1] = linierColorFunc(value)
  } else if (value <= -minimumValue) {
    base = backGroundNegaLch
    base[1] = linierColorFunc(-value)
  } else {
    base = backGroundEvenLch
  }
  return rgb2hex(lab2rgb(lch2lab(base)))
}
export default getRgb

export const rgb2hex = (rgb: number[]) =>
  '#' + rgb.map((value: number) => ('0' + Math.round(value).toString(16)).slice(-2)).join('')

//sRGBからL*a*b*に変換する
const rgb2lab = (rgb: number[]) => {
  const [r, g, b] = rgb
    .map(d => d / 255.0)
    .map(d => (d > 0.04045 ? Math.pow((d + 0.055) / 1.055, 2.4) : d / 12.92))
  const [x, y, z] = [
    (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047,
    r * 0.2126 + g * 0.7152 + b * 0.0722,
    (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883
  ].map(d => (d > 0.008856 ? Math.cbrt(d) : 7.787 * d + 16.0 / 116.0))
  return [116.0 * y - 16.0, 500.0 * (x - y), 200.0 * (y - z)]
}

// L*a*b*からsRGBに変換する
const lab2rgb = (lab: number[]) => {
  const [l, a, b] = lab
  const y = l <= 8 ? (l * 100.0) / 903.3 : 100.0 * Math.pow((l + 16.0) / 116.0, 3)
  const y2 = l <= 8 ? 7.787 * (y / 100.0) + 16.0 / 116.0 : Math.cbrt(y / 100)
  const x =
    a / 500.0 + y2 <= 0.2069
      ? (95.047 * (a / 500 + y2 - 16 / 116)) / 7.787
      : 95.047 * Math.pow(a / 500 + y2, 3)
  const z =
    y2 - b / 200.0 <= 0.2059
      ? (108.883 * (y2 - b / 200 - 16 / 116)) / 7.787
      : 108.883 * Math.pow(y2 - b / 200, 3)
  const [x1, y1, z1] = [x, y, z].map(d => d / 100)
  return [
    x1 * 3.2406 + y1 * -1.5372 + z1 * -0.4986,
    x1 * -0.9689 + y1 * 1.8758 + z1 * 0.0415,
    x1 * 0.0557 + y1 * -0.204 + z1 * 1.057
  ].map(
    d =>
      Math.min(1, Math.max(0, d > 0.0031308 ? 1.055 * Math.pow(d, 1.0 / 2.4) - 0.055 : d * 12.92)) *
      255.0
  )
}

// L*a*b*からL*C*H*に変換する
const lab2lch = (lab: number[]) => {
  const norm = (x: number, y: number) => Math.sqrt(x * x + y * y)
  const rad2deg = (rad: number) => (rad * 180) / Math.PI
  return [lab[0], norm(lab[1], lab[2]), rad2deg(Math.atan2(lab[2], lab[1]))]
}

// L*C*H*からL*a*b*に変換する
const lch2lab = (lch: number[]) => {
  const rad = (lch[2] * Math.PI) / 180.0
  return [lch[0], lch[1] * Math.cos(rad), lch[1] * Math.sin(rad)]
}

// RGB2色のコントラストを求める
const contrast = (rgb1: number[], rgb2: number[]) => {
  const g = (d: number) => (d <= 0.03928 ? d / 12.98 : Math.pow((d + 0.055) / 1.055, 2.4))
  const rColorL = (C: number[]) =>
    0.2126 * g(C[0] / 255.0) + 0.7152 * g(C[1] / 255.0) + 0.0722 * g(C[2] / 255.0)
  const result = [rColorL(rgb1) + 0.05, rColorL(rgb2) + 0.05].sort()
  return result[1] / result[0]
}

// CIE 1976 L*a*b* 空間におけるCIEDE2000色差を求めます
const colorDiffCIEDE2000 = (lab1: number[], lab2: number[]) => {
  const norm = (x: number, y: number) => Math.sqrt(x * x + y * y)
  const tolerance_zero = (x: number) => Math.abs(x) < 0.00000001
  const cosd = (deg: number) => Math.cos((deg * Math.PI) / 180)
  const sind = (deg: number) => Math.sin((deg * Math.PI) / 180)
  const reg_fqatan = (deg: number) => (deg >= 0 ? deg : deg + 360.0)
  const fqatan = (y: number, x: number) => reg_fqatan((Math.atan2(y, x) * 180.0) / Math.PI)
  const f7 = (x: number) =>
    x < 1.0 ? Math.pow(x / 25.0, 3.5) : 1.0 / Math.sqrt(1.0 + Math.pow(25.0 / x, 7.0))
  const [L1, a1, b1] = lab1
  const [L2, a2, b2] = lab2
  const epsilon = 0.000000001
  const C1ab = norm(a1, b1)
  const C2ab = norm(a2, b2)
  const Cab = (C1ab + C2ab) / 2.0
  const G = 0.5 * (1.0 - f7(Cab))
  const a1_ = (1.0 + G) * a1
  const a2_ = (1.0 + G) * a2
  const C1_ = norm(a1_, b1)
  const C2_ = norm(a2_, b2)
  const h1_ = tolerance_zero(a1_) && tolerance_zero(b1) ? 0.0 : fqatan(b1, a1_)
  const h2_ = tolerance_zero(a2_) && tolerance_zero(b2) ? 0.0 : fqatan(b2, a2_)
  const dL_ = L2 - L1
  const dC_ = C2_ - C1_
  const C12 = C1_ * C2_
  let dh_ = 0.0
  if (!tolerance_zero(C12)) {
    const tmp = h2_ - h1_
    if (Math.abs(tmp) <= 180.0 + epsilon) {
      dh_ = tmp
    } else if (tmp > 180.0) {
      dh_ = tmp - 360.0
    } else if (tmp < -180.0) {
      dh_ = tmp + 360.0
    }
  }
  const dH_ = 2.0 * Math.sqrt(C12) * sind(dh_ / 2.0)
  const L_ = (L1 + L2) / 2.0
  const C_ = (C1_ + C2_) / 2.0
  let h_ = h1_ + h2_
  if (!tolerance_zero(C12)) {
    const tmp1 = Math.abs(h1_ - h2_)
    const tmp2 = h1_ + h2_
    if (tmp1 <= 180.0 + epsilon) {
      h_ = tmp2 / 2.0
    } else if (tmp2 < 360.0) {
      h_ = (tmp2 + 360.0) / 2.0
    } else if (tmp2 >= 360.0) {
      h_ = (tmp2 - 360.0) / 2.0
    }
  }
  const T =
    1.0 -
    0.17 * cosd(h_ - 30.0) +
    0.24 * cosd(2.0 * h_) +
    0.32 * cosd(3.0 * h_ + 6.0) -
    0.2 * cosd(4.0 * h_ - 63.0)
  const dTh = 30.0 * Math.exp(-Math.pow((h_ - 275.0) / 25.0, 2.0))
  const L_2 = (L_ - 50.0) * (L_ - 50.0)
  const RC = 2.0 * f7(C_)
  const SL = 1.0 + (0.015 * L_2) / Math.sqrt(20.0 + L_2)
  const SC = 1.0 + 0.045 * C_
  const SH = 1.0 + 0.015 * C_ * T
  const RT = -sind(2.0 * dTh) * RC
  const kL = 1.0 // These are proportionally coefficients
  const kC = 1.0 // and vary according to the condition.
  const kH = 1.0 // These mostly are 1.
  const LP = dL_ / (kL * SL)
  const CP = dC_ / (kC * SC)
  const HP = dH_ / (kH * SH)
  return Math.sqrt(LP * LP + CP * CP + HP * HP + RT * CP * HP)
}
