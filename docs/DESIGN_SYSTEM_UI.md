# DESIGN SYSTEM — UI CONTRACT

## 0. Purpose
Defines visual, interaction and component rules for the UI.
Modules MUST consume shared components and tokens.

---

## 1. Visual Principles
- Enterprise SaaS / Fintech
- Minimalist, high whitespace
- Soft borders and subtle shadows
- Consistency over creativity

---

## 2. Color Tokens

### Brand
- Primary: #7C5CFF

### Backgrounds
- App Background: #F6F7FB
- Surface (Cards): #FFFFFF
- Sidebar: #F2F3F8

### Text
- Primary: #0F172A
- Muted: #64748B

### Borders
- Default: #E2E8F0

### Semantic (Soft)
| Type | FG | BG |
|---|---|---|
| Success | #16A34A | #EAFBF1 |
| Warning | #D97706 | #FFF7E6 |
| Error | #DC2626 | #FFECEC |
| Overdue | #EA580C | #FFF0E8 |
| Info | #0EA5E9 | #E7F6FF |

Rule: never use flat saturated backgrounds for statuses.

---

## 3. Typography

- Font family: Inter

| Usage | Size | Weight |
|---|---|---|
| H1 | 24px | 700 |
| H2 | 18px | 600 |
| H3 | 16px | 600 |
| Body | 14px | 400–500 |
| Label | 12px | 500 |

---

## 4. Spacing & Radius
- Base spacing unit: 4px
- Component padding: 16–20px
- Section spacing: 24–32px
- Radius:
  - sm: 10px
  - md: 12px
  - lg: 16px

---

## 5. Components Rules

### Buttons
- Primary:
  - Height 40px
  - bg-primary
  - text-white
  - rounded-xl
- Secondary:
  - White background
  - Neutral border

### Inputs
- Height 40px
- Border neutral
- Focus ring primary

### Tables
- Row hover highlight
- Soft separators
- Status via semantic badges

---

## 6. States
- Loading: skeletons
- Empty: explanation + primary CTA
- Error: banner with retry
