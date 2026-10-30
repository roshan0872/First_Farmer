# First Farmer Agriculture System &mdash; Multilingual Translation Review

## 1. Overview
The platform supports three languages:
- **English (`en`)**: Primary native source language (100% complete).
- **Tamil (`ta`)**: Dravidian language with full Noto Sans Tamil typography support.
- **Hindi (`hi`)**: Devanagari script with full Noto Sans Devanagari typography support.

---

## 2. Translation Coverage Report

### A. User Interface & Navigation Strings (`app/i18n/`)
| UI Domain | English (`en.json`) | Tamil (`ta.json`) | Hindi (`hi.json`) | Status |
|---|---|---|---|---|
| Main Navigation Links | 100% | 100% | 100% | Verified |
| Buttons & Actions | 100% | 100% | 100% | Verified |
| Authentication & Forms | 100% | 100% | 100% | Verified |
| Validation & Error Messages | 100% | 100% | 100% | Verified |
| Recommendation Engine UI | 100% | 100% | 100% | Verified |
| Weather & Advisory UI | 100% | 100% | 100% | Verified |
| Chatbot UI & Disclaimers | 100% | 100% | 100% | Verified |

### B. Database Crop Content (`translations` table)
| Crop Entity | Common Name (TA) | Common Name (HI) | Overview Desc (TA) | Overview Desc (HI) | Review State |
|---|---|---|---|---|---|
| **Rice (Paddy)** | நெல் (அரிசி) | धान (चावल) | Translated | Translated | Machine-assisted |
| **Wheat** | கோதுமை | गेहूँ | Translated | Translated | Machine-assisted |
| **Maize (Corn)** | மக்காச்சோளம் | मक्का | Translated | Translated | Machine-assisted |
| **Tomato** | தக்காளி | टमाटर | Translated | Translated | Machine-assisted |
| **Cotton** | பருத்தி | कपास | Translated | Translated | Machine-assisted |
| **Banana** | வாழை | केला | Translated | Translated | Machine-assisted |
| **Sugarcane** | கரும்பு | गन्ना | Translated | Translated | Machine-assisted |
| **Groundnut** | நிலக்கடலை | मूंगफली | Translated | Translated | Machine-assisted |
| **Finger Millet (Ragi)** | கேழ்வரகு | रागी / मडुआ | Translated | Translated | Machine-assisted |
| **Green Gram (Pulses)** | பாசிப்பயறு | मूंग (दाल) | Translated | Translated | Machine-assisted |

---

## 3. Scope & Untranslated Content Notice
In accordance with professional agronomic standards:
- Scientific botanical and entomological Latin binomials (e.g. *Oryza sativa*, *Scirpophaga incertulas*, *Helicoverpa armigera*) and international measurement units (°C, mm, kg/ha) are intentionally left untranslated across all locales to preserve exact scientific meaning.
- Highly specialized sub-guide paragraphs (seed chemical concentrations, exact soil mechanical properties) are rendered in English when an authentic regional language translation is unavailable, accompanied by the visible user alert:
  > **Notice:** *"This content is currently available in English only."*

---

## 4. Native Speaker Review Instructions
Translators and native reviewers should verify:
1. Agronomic terminology naturalness (e.g., ensuring "Transplanting" in Tamil uses traditional term *நடவு* rather than literal translation).
2. Devanagari conjunct rendering and diacritic clarity.
3. Formatting consistency across responsive mobile screen widths.
