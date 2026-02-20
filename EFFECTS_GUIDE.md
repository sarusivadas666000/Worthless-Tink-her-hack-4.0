# 🎬 3D Camera Effects - Visual Guide

## Effect Graphics & Explanations

### 1. 🔍 Zoom/Dolly Effect

```
Frame State              Visual Result
─────────────────       ──────────────────

Start:  [CAMERA]──────  Image zoomed out
        [   IMG   ]     
                        
Mid:    [CAMERA]        Image zooming in
        [ IMG ]         (closer perspective)
                        
End:    [CAMERA]        Image zoomed in
        [IMG]           (fullscreen view)
```

**Mathematics**:
```
zoom = 1.0 + 0.15 × sin(progress × π × 3)
Range: 0.85x to 1.15x scale
```

**Effect**: Makes product appear to move toward/away from camera
**Use Case**: Creates depth and draws attention

---

### 2. ↔️ Pan/Camera Movement

```
Left Pan:           Right Pan:          Vertical Pan:
───────────────    ───────────────    ───────────────
↗ ◼ ◼ ◼            ◼ ◼ ◼ ↖            ↓ ◼ ◼ ◼
  ◼ IMG ◼      →     ◼ IMG ◼      →    ◼ IMG ◼
  ◼ ◼ ◼              ◼ ◼ ◼              ◼ ◼ ◼ ↑
```

**Mathematics**:
```
pan_x = 25 × sin(progress × 2π)
pan_y = 25 × cos(progress × 2π)
Movement: ±25 pixels in X,Y axes
```

**Effect**: Camera scans across the image
**Use Case**: Reveals different parts of product

---

### 3. 🎲 3D Perspective / Tilt

```
Top View:           Side View:          Diagonal Tilt:
───────────────    ───────────────    ───────────────
  ┌─────────┐        ┌─────────┐         ╱───────╲
  │ PRODUCT │        │ PRODUCT │        ╱ PRODUCT ╲
  └─────────┘        └─────────┘      ╱___________╲
  (normal)      →    (tilted up)       (perspectiv)
```

**Mathematics**:
```
Rotation matrices (Euler angles):
α (X-axis): ±15°  (up/down tilt)
β (Y-axis): ±20°  (left/right rotation)
γ (Z-axis): ±10°  (spin)
```

**Effect**: Image appears to rotate in 3D space
**Use Case**: Makes 2D image feel 3D

---

### 4. 🔄 Full 3D Rotation

```
360° Spin Animation:

Frame 1:    Frame 2:    Frame 3:    Frame 4:
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│ TOP │    ╱  90° ╲   │ TOP │    ╱ 270°╲
└─────┘   ╱________╲  └─────┘   ╱______╲
  0°                 180°            360°
```

**Effect**: Product spins 360 degrees smoothly
**Animation**: Full rotation over video duration
**Use Case**: Showcase all sides of product

---

### 5. 💨 Motion Blur

```
No Blur              Light Blur         Heavy Blur
(sharp)              (natural)          (cinematic)

─────────────       ───────────────     ──────────────
│ ▓▓▓▓▓▓▓ │        │ ▓▓▓▓▓▓▓▓░░ │     │ ▓▓▓▓▓░░░░░ │
│ ▓OBJECT▓ │   →   │ ▓OBJECT▓░░ │  →  │ ▓OBJECT░░░ │
│ ▓▓▓▓▓▓▓ │        │ ▓▓▓▓▓▓▓▓░░ │     │ ▓▓▓▓▓░░░░░ │
───────────────     ───────────────     ──────────────
```

**Physics**:
```
Blur kernel: 3-10 pixels (variable with animation)
Effect: Like camera movement has "weight"
```

**Visual Result**: Smooth, cinematic feel
**Use Case**: Professional video appearance

---

### 6. 👁️ Depth of Field (Focus Blur)

```
Without DOF:         With DOF:
(everything sharp)   (background blurred)

───────────────      ───────────────
│ ▓ ▓ ▓ ▓ ▓ │       │ ░ ░ ░ ░ ░ │
│ ▓ PRD ▓ │   →     │ ░ PRD ░ │
│ ▓ ▓ ▓ ▓ ▓ │       │ ░ ░ ░ ░ ░ │
───────────────      ───────────────
```

**Effect**: 
- Product stays sharp
- Background gradually blurs
- Focus point moves during animation

**Mathematical Model**:
```
mask = 1.0 - clip(distance_from_focus / 200, 0, 1)
result = sharp × mask + blurred × (1 - mask)
```

**Visual Result**: Real camera lens behavior
**Use Case**: Premium product showcase

---

### 7. 🌈 Chromatic Aberration

```
Original:           RGB Split:
───────────────    ───────────────
│  ▓▓▓  │          │░▓▓▓░ │
│ ▓▓ ▓▓ │   →      │░▓▓▓░ │
│  ▓▓▓  │          │░▓▓▓░ │
───────────────    ───────────────

(Red channel +5px right)
(Blue channel -5px left)
(Green centered)
```

**Shift Pattern**:
```
Red:   x + 5
Green: x + 0  
Blue:  x - 5
```

**Visual Effect**: Sci-fi, cyberpunk appearance
**Use Case**: Tech products, gaming, modern marketing

---

## Combined Effects Timeline

### "Full Cinematic" Configuration
```
Time 0%:   Fade Start + Zoom Out + Pan Left
Timeline:   |███░░░░░░░░░░░░░░░░░░░░|
            ├─ Perspective tilt ──┘
            ├─ Motion blur throughout
            └─ Color glitch (optional)

Time 50%:  Peak Effect + All Transforms Active
Timeline:   |░░░████████░░░░░░░░░░░░░|
            ├─ Zoom in progress
            ├─ Pan from left to right
            ├─ 3D rotation peak
            └─ DOF focus moving

Time 100%: Fade End + Zoom In + Pan Right
Timeline:   |░░░░░░░░░░░░░░░░░░│████|
            ├─ Perspective center
            ├─ Motion blur fading
            └─ Final angle resolved
```

---

## Effect Mathematics

### Sine Wave Animation
```python
# Smooth oscillation from 0 to 1 to 0
value = sin(progress × π)

# Faster oscillation (cycles multiple times)
value = sin(progress × 2π × cycles)

# Peak at middle
value = sin(progress × π) if progress < 0.5 else sin((1-progress) × π)
```

### Transform Chain
```
For each frame:
  1. output = input_image
  2. if perspective: output = perspective_transform(output)
  3. if zoom: output = dolly_camera(output)
  4. if pan: output = translate(output)
  5. if rotation: output = rotate(output)
  6. if motion_blur: output = gaussian_blur(output)
  7. if dof: output = selective_blur(output)
  8. if chroma: output = rgb_aberration(output)
  return output
```

---

## Visual Configuration Examples

### "Classic Product Showcase"
```json
{
  "zoom": true,
  "pan": true,
  "rotation": false,
  "perspective": true,
  "motion_blur": true,
  "depth_of_field": false,
  "chromatic_aberration": false
}
```
**Result**: Professional, clean, elegant

### "Action-Packed"
```json
{
  "zoom": true,
  "pan": true,
  "rotation": true,
  "perspective": true,
  "motion_blur": true,
  "depth_of_field": false,
  "chromatic_aberration": false
}
```
**Result**: Dynamic, exciting, attention-grabbing

### "Premium Luxury"
```json
{
  "zoom": true,
  "pan": true,
  "rotation": false,
  "perspective": true,
  "motion_blur": true,
  "depth_of_field": true,
  "chromatic_aberration": false
}
```
**Result**: High-end, sophisticated, cinematic

### "Tech/Futuristic"
```json
{
  "zoom": true,
  "pan": true,
  "rotation": true,
  "perspective": true,
  "motion_blur": true,
  "depth_of_field": false,
  "chromatic_aberration": true
}
```
**Result**: Modern, cutting-edge, scientific

### "Subtle & Smooth"
```json
{
  "zoom": false,
  "pan": false,
  "rotation": false,
  "perspective": false,
  "motion_blur": true,
  "depth_of_field": false,
  "chromatic_aberration": false
}
```
**Result**: Clean fade transition with slight blur

---

## Performance Impact

### Effect Computation Time per Frame
| Effect | Time | Notes |
|--------|------|-------|
| Perspective | 45ms | Matrix calculations |
| Zoom | 30ms | Crop + resize |
| Pan | 20ms | Affine transform |
| Rotation | 40ms | OpenCV warpAffine |
| Motion Blur | 35ms | Gaussian kernel |
| DOF | 50ms | Multiple blurs + blend |
| Chromatic Aberration | 25ms | Channel shifts |
| **Total (all 7)** | **245ms** | ~60 frames @ 24fps |

**Optimization**: Most effects can run in parallel;
sequential reduces from 245ms to ~150ms per frame.

---

## Recommendations

### For E-Commerce
✓ Use: Zoom, Pan, Perspective, Motion Blur
✗ Skip: Rotation, DOF, Chromatic Aberration
→ **Why**: Professional but exciting

### For Luxury Goods
✓ Use: Zoom, Pan, Perspective, Motion Blur, DOF
✗ Skip: Rotation, Chromatic Aberration
→ **Why**: Elegant and sophisticated

### For Tech Products
✓ Use: All effects
→ **Why**: Modern, cutting-edge appearance

### For Social Media
✓ Use: Zoom, Rotation, Motion Blur
✗ Skip: DOF (doesn't share well)
→ **Why**: Eye-catching in feed

---

## Customization Tips

1. **Increase Effect Intensity**
   - Adjust angle values in perspective_transform
   - Increase pan_amount and zoom_range
   - Boost motion blur by changing kernel size

2. **Reduce Effect Speed**
   - Lower animation progress multiplier
   - Increase FRAME_COUNT for smoother transitions
   - Change FPS for slower/faster playback

3. **Create Signature Look**
   - Combine specific effects
   - Use same configuration for brand consistency
   - Test with your product images

---

**Master the effects! 🎬✨**
