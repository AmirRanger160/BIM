# Quick Testing Checklist for GeoBiro Animations

## Desktop Testing (1024px+)

### Animations on Page Load
- [ ] Hero title fades in smoothly
- [ ] Hero paragraph fades in (0.2s after title)
- [ ] Hero buttons fade in (0.4s after paragraph)
- [ ] All fade-ins reach opacity: 1 without scale artifacts

### Scroll-Triggered Animations
- [ ] Stats cards fade in + slide up when scrolling to them
- [ ] Service cards (BIM) fade in + slide up on scroll
- [ ] Service cards (Surveying) fade in + slide up on scroll
- [ ] About section content fades in on scroll
- [ ] Team member cards appear with stagger effect
- [ ] Certificates/Licenses/History cards animate on scroll
- [ ] CTA section items animate on scroll
- [ ] Contact form and map animate on scroll

### Button & Interactive Hover States
- [ ] Primary buttons: Scale(1.02) + shadow depth increase
- [ ] Play button: Scale(1.1) with glow shadow
- [ ] Service cards: translateY(-8px) + image scale(1.03)
- [ ] Team member images: scale(1.08) zoom
- [ ] About feature boxes: Background highlight + translateX
- [ ] Logo: scale(1.05) on hover
- [ ] Navigation links: Underline animates from 0 to 100% width

### Smooth Scrolling
- [ ] Navigation links smooth scroll to sections
- [ ] No jank or layout shift during scroll
- [ ] Animations maintain 60fps (Chrome DevTools)

---

## Tablet Testing (768px - 1023px)

### Layout Responsiveness
- [ ] Service grid: 3 columns → 2 columns
- [ ] Team grid: 6 columns → 3 columns
- [ ] About section: Side-by-side → Stacked
- [ ] Contact form: Side-by-side → Stacked
- [ ] Padding/margins adjusted appropriately

### Touch Target Sizes
- [ ] All buttons: Minimum 44px height
- [ ] Form inputs: Minimum 44px height
- [ ] Navigation items: 44px+ minimum
- [ ] Link padding comfortable for touch

### Hamburger Menu NOT Visible
- [ ] Hamburger icon should NOT appear at 768px
- [ ] Desktop navigation still visible
- [ ] Navigation links clickable

---

## Mobile Testing (≤768px)

### Hamburger Menu Display
- [ ] Hamburger menu icon appears (three lines)
- [ ] Desktop navigation nav (.nav-desktop) is HIDDEN
- [ ] Logo still visible

### Hamburger Toggle Interaction
- [ ] Click hamburger → menu slides in from right
- [ ] Icon transforms: Top line rotates 45°, bottom rotates -45°, middle fades
- [ ] Click again → menu slides out, icon returns to normal
- [ ] Overlay appears when menu is open
- [ ] Overlay click closes menu

### Mobile Navigation Menu
- [ ] Menu slides from RIGHT side (RTL compatible)
- [ ] Full-height overlay menu
- [ ] Vertical navigation items
- [ ] Menu items: "صفحه اول", "خدمات BIM", etc. visible
- [ ] Each link is at least 44px tall
- [ ] Links clickable and functional

### Menu Closing
- [ ] Click any navigation link → menu closes + smooth scroll to section
- [ ] Click overlay → menu closes
- [ ] Press Escape key → menu closes
- [ ] Menu should only close on these three triggers

### Form Responsiveness
- [ ] Form inputs stack vertically
- [ ] Full width on mobile
- [ ] Input padding: 12px or more
- [ ] Button width: Full or good size for mobile
- [ ] Touch targets clearly separated

### Grid Responsiveness
- [ ] Service cards: 1 column (≤768px)
- [ ] Team grid: 2 columns (≤480px)
- [ ] Stats grid: 2 columns (≤768px) → 1 column (≤480px)
- [ ] Certificates: 1 column
- [ ] Licenses: 1 column
- [ ] History: 1 column

### Font Sizes
- [ ] Section titles: Smaller but readable
- [ ] Body text: Clear without zooming
- [ ] Button text: Legible

---

## RTL (Right-to-Left) Direction Testing

### Visual Direction
- [ ] All text flows right to left
- [ ] Numbers in Persian script (۱۰۰۰+, etc.)
- [ ] Layouts mirror naturally

### Navigation Direction
- [ ] Desktop nav items aligned right with row-reverse
- [ ] Hamburger menu slides from RIGHT (not left)
- [ ] Mobile overlay menu items aligned right

### Animation Direction
- [ ] Slide animations feel natural in RTL
- [ ] Hamburger menu slide: 100% offset from right
- [ ] No visual jank or unexpected directions

---

## Performance Testing (Chrome DevTools)

### Frame Rate
- [ ] Scroll animations: 60fps minimum
- [ ] Hover interactions: 60fps
- [ ] Page load animations: 60fps
- [ ] No frame drops or jank visible

### Performance Metrics
- [ ] Cumulative Layout Shift (CLS): 0 (no movement)
- [ ] No repaints on scroll (transform/opacity only)
- [ ] First Contentful Paint: Fast

### Animation Profiling
- [ ] Open DevTools → Performance tab
- [ ] Record scroll action
- [ ] Check timeline: All frames 60fps
- [ ] No layout shift warnings
- [ ] GPU acceleration active

---

## Accessibility Testing

### Touch Targets
- [ ] All clickable elements ≥ 44px
- [ ] Buttons clearly distinguishable
- [ ] Links have sufficient color contrast

### Keyboard Navigation
- [ ] Tab through navigation works
- [ ] Escape key closes hamburger menu
- [ ] Focus indicators visible
- [ ] Smooth scroll doesn't break tab order

### Form Accessibility
- [ ] Input labels clear
- [ ] Focus states visible (border glow)
- [ ] Placeholder text readable

---

## Browser Compatibility Checklist

| Browser | Desktop | Mobile | Notes |
|---------|---------|--------|-------|
| Chrome  | ✓       | ✓      | Full support |
| Firefox | ✓       | ✓      | Full support |
| Safari  | ✓       | ✓      | Full support |
| Edge    | ✓       | ✓      | Full support |
| IE 11   | ✗       | N/A    | No Intersection Observer |

---

## Specific Animation Tests

### Intersection Observer
```javascript
// Open Console and scroll to trigger animations
// You should see console messages when sections come into view
// (if console logging is added)
```

### CSS Animation Performance
```
1. Open DevTools → Rendering
2. Check "Paint flashing"
3. Scroll page → Only see paint on new elements
4. Transform animations should NOT show paint
```

### Transform vs Layout
```
Good (No Layout Shift):
- transform: translateY(-8px)
- opacity: 0.5
- transform: scale(1.1)

Bad (Layout Shift):
- padding: 20px (avoid)
- width: 100% (avoid)
- height: 44px change (avoid)
```

---

## Test Scenarios

### Scenario 1: Fresh Page Load
1. Open website on desktop
2. Hero elements should fade in sequentially
3. Scroll down slowly
4. Each section should animate as it enters viewport
5. Check console for no errors

### Scenario 2: Mobile Menu Navigation
1. Open on mobile (≤768px)
2. Tap hamburger icon
3. Menu slides from right
4. Tap any menu item
5. Smooth scroll to section
6. Menu closes automatically
7. Repeat with different menu items

### Scenario 3: Hover Interactions
1. On desktop, hover over buttons
2. They should scale up slightly
3. Shadow should deepen
4. Transition should be smooth
5. Repeat with service cards, buttons, links

### Scenario 4: Responsive Breakpoint Test
1. Open DevTools Responsive Design Mode
2. Set width to 1024px → 768px
3. Watch layouts reflow
4. Check navigation changes
5. Set to ≤480px
6. Verify mobile-optimized layout

### Scenario 5: Scroll Performance
1. Use DevTools Performance tab
2. Record a 5-second scroll
3. Analyze flame chart
4. Confirm 60fps throughout
5. Zero layout shift indicators

---

## Known Good States

### Desktop (1024px+)
✓ Desktop navigation visible
✓ Service grids: 3 columns
✓ Team: 6 columns
✓ No hamburger menu
✓ Hover animations active

### Tablet (768px - 1023px)
✓ Navigation still desktop style
✓ Service grids: 2 columns
✓ Team: 3 columns
✓ No hamburger menu yet
✓ Hover animations active

### Mobile (≤768px)
✓ Hamburger menu visible
✓ Desktop nav hidden
✓ Service grids: 1 column
✓ Team: 2 columns
✓ Form full width
✓ Touch-optimized

### Extra Small (≤480px)
✓ Hamburger menu visible
✓ Team: 2 columns
✓ Stats: 1 column
✓ Minimal padding
✓ Touch-optimized

---

## Troubleshooting Guide

### Issue: Animations not showing
- [ ] Check animations.css is imported in App.vue
- [ ] Verify class names are correct (animate-on-scroll)
- [ ] Check for CSS errors in DevTools
- [ ] Verify Intersection Observer is supported

### Issue: Hamburger menu not appearing
- [ ] Check media query: `@media (max-width: 768px)`
- [ ] Verify `display: flex` on .hamburger
- [ ] Check z-index: should be 1001 for hamburger
- [ ] Use DevTools to toggle mobile view

### Issue: Animations look janky
- [ ] Check DevTools Performance for 60fps
- [ ] Verify no layout properties (width/height) animating
- [ ] Check for excessive repaints
- [ ] Disable extensions if needed

### Issue: RTL not working
- [ ] Verify `direction: rtl` on body/app
- [ ] Check transform directions (translate3d(100%, 0, 0))
- [ ] No hardcoded `left` values
- [ ] Use `right` for positioning

---

**Last Updated:** December 23, 2025
**Status:** Ready for QA Testing ✅
