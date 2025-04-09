const fs = require('fs');

const allowedRanges = [
  [0, 127], // Basic Latin
  [128, 255], // Latin-1 Supplement
  [256, 383], // Latin Extended-A
  [384, 591], // Latin Extended-B
  [592, 687], // IPA Extensions
  [688, 767], // Spacing Modifier Letters
  [768, 879], // Combining Diacritical Marks
  [880, 1023], // Greek and Coptic
  [1024, 1279], // Cyrillic
  [1280, 1327], // Cyrillic Supplement
  [1328, 1423], // Armenian
  [1424, 1535], // Hebrew
  [1536, 1791], // Arabic
  [1792, 1871], // Syriac
  [1872, 1919], // Arabic Supplement
  [1920, 1983], // Thaana
  [1984, 2047], // NKo
  [2048, 2111], // Samaritan
  [2112, 2143], // Mandaic
  [2144, 2159], // Syriac Supplement
  [2208, 2303], // Arabic Extended-A
  [2304, 2431], // Devanagari
  [2432, 2559], // Bengali
  [2560, 2687], // Gurmukhi
  [2688, 2815], // Gujarati
  [2816, 2943], // Oriya
  [2944, 3071], // Tamil
  [3072, 3199], // Telugu
  [3200, 3327], // Kannada
  [3328, 3455], // Malayalam
  [3456, 3583], // Sinhala
  [3584, 3711], // Thai
  [3712, 3839], // Lao
  [3840, 4095], // Tibetan
  [4096, 4255], // Myanmar
  [4256, 4351], // Georgian
  [4352, 4607], // Hangul Jamo
  [4608, 4991], // Ethiopic
  [4992, 5023], // Ethiopic Supplement
  [5024, 5119], // Cherokee
  [5120, 5503], // Unified Canadian Aboriginal Syllabics
  [5504, 5535], // Ogham
  [5536, 5631], // Runic
  [5632, 5663], // Tagalog
  [5664, 5695], // Hanunoo
  [5696, 5727], // Buhid
  [5728, 5759], // Tagbanwa
  [5760, 5887], // Khmer
  [5888, 6063], // Mongolian
  [6064, 6143], // Unified Canadian Aboriginal Syllabics Extended
  [6144, 6223], // Limbu
  [6224, 6399], // Tai Le + New Tai Lue
  [6400, 6431], // Khmer Symbols
  [6656, 6783], // Tai Tham
  [6784, 6847], // Combining Diacritical Marks Extended
  [6912, 7039], // Balinese
  [7040, 7103], // Sundanese
  [7104, 7167], // Batak
  [7168, 7247], // Lepcha
  [7248, 7295], // Ol Chiki
  [7296, 7311], // Cyrillic Extended-C
  [7312, 7359], // Georgian Extended
  [7360, 7375], // Sundanese Supplement
  [7376, 7423], // Vedic Extensions
  [7424, 7551], // Phonetic Extensions
  [7552, 7615], // Phonetic Extensions Supplement
  [7616, 7679], // Combining Diacritical Marks Supplement
  [7680, 7935], // Latin Extended Additional
  [7936, 8191], // Greek Extended
  [8192, 8303], // General Punctuation
  [8304, 8351], // Superscripts and Subscripts
  [8352, 8399], // Currency Symbols
  [8400, 8447], // Combining Diacritical Marks for Symbols
  [8448, 8527], // Letterlike Symbols
  [8528, 8591], // Number Forms
  [8592, 8703], // Arrows
  [8704, 8959], // Mathematical Operators
  [8960, 9215], // Miscellaneous Technical
  [9216, 9279], // Control Pictures
  [9280, 9311], // Optical Character Recognition
  [9312, 9471], // Enclosed Alphanumerics
  [9472, 9599], // Box Drawing
  [9600, 9631], // Block Elements
  [9632, 9727], // Geometric Shapes
  [9728, 9983], // Miscellaneous Symbols
  [9984, 10175], // Dingbats
  [10176, 10223], // Miscellaneous Mathematical Symbols-A
  [10224, 10239], // Supplemental Arrows-A
  [10240, 10495], // Braille Patterns
  [10496, 10623], // Supplemental Arrows-B
  [10624, 10751], // Miscellaneous Mathematical Symbols-B
  [10752, 11007], // Supplemental Mathematical Operators
  [11008, 11263], // Miscellaneous Symbols and Arrows
  [11264, 11359], // Glagolitic
  [11360, 11391], // Latin Extended-C
  [11392, 11519], // Coptic
  [11520, 11567], // Georgian Supplement
  [11568, 11647], // Tifinagh
  [11648, 11743], // Ethiopic Extended
  [11744, 11775], // Cyrillic Extended-A
  [11776, 11903], // Supplemental Punctuation
  [11904, 12031], // CJK Radicals Supplement
  [12032, 12255], // Kangxi Radicals
  [12272, 12287], // Ideographic Description Characters
  [12288, 12351], // CJK Symbols and Punctuation
  [12352, 12447], // Hiragana
  [12448, 12543], // Katakana
  [12544, 12591], // Bopomofo
  [12592, 12687], // Hangul Compatibility Jamo
  [12688, 12703], // Kanbun
  [12704, 12735], // Bopomofo Extended
  [12736, 12783], // CJK Strokes
  [12784, 12799], // Katakana Phonetic Extensions
  [12800, 13055], // Enclosed CJK Letters and Months
  [13056, 13311], // CJK Compatibility
  [13312, 19903], // CJK Unified Ideographs Extension A
  [19904, 19967], // Yijing Hexagram Symbols
  [19968, 40959], // CJK Unified Ideographs
  [40960, 42127], // Yi Syllables
  [42128, 42191], // Yi Radicals
  [42192, 42239], // Lisu
  [42240, 42303], // Vai
  [42304, 42399], // Cyrillic Extended-B
  [42400, 42495], // Bamum
  [42496, 42527], // Modifier Tone Letters
  [42528, 42751], // Latin Extended-D
  [42752, 42783], // Syloti Nagri
  [42784, 42815], // Common Indic Number Forms
  [42816, 43007], // Phags-pa
  [43008, 43055], // Saurashtra
  [43056, 43071], // Devanagari Extended
  [43072, 43135], // Kayah Li
  [43136, 43183], // Rejang
  [43184, 43231], // Hangul Jamo Extended-A
  [43232, 43263], // Javanese
  [43264, 43311], // Myanmar Extended-B
  [43312, 43359], // Cham
  [43360, 43391], // Myanmar Extended-A
  [43392, 43487], // Tai Viet
  [43488, 43519], // Meetei Mayek Extensions
  [43520, 43583], // Ethiopic Extended-A
  [43584, 43631], // Latin Extended-E
  [43632, 43743], // Cherokee Supplement
  [43744, 43775], // Meetei Mayek
  [44032, 55215], // Hangul Syllables
  [55216, 55295], // Hangul Jamo Extended-B
  [57344, 63743], // Private Use Area
  [63744, 64255], // CJK Compatibility Ideographs
  [64256, 64335], // Alphabetic Presentation Forms
  [64336, 65023], // Arabic Presentation Forms-A
  [65024, 65039], // Variation Selectors
  [65040, 65055], // Vertical Forms
  [65056, 65071], // Combining Half Marks
  [65072, 65103], // CJK Compatibility Forms
  [65104, 65135], // Small Form Variants
  [65136, 65279], // Arabic Presentation Forms-B
  [65280, 65519], // Halfwidth and Fullwidth Forms
  [65520, 65535], // Specials



];

const allAllowedCodePoints = [];

for (const [start, end] of allowedRanges) {
  for (let code = start; code <= end; code++) {
    allAllowedCodePoints.push(code);
  }
}

// שמירת התוצאה לקובץ JSON
fs.writeFileSync('allowed_codepoints.json', JSON.stringify(allAllowedCodePoints, null, 2));

console.log('✔️ קובץ allowed_codepoints.json נוצר בהצלחה!');
