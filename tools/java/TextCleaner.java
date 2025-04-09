
import java.io.*;
import java.util.*;

public class TextCleaner {

    public static void main(String[] args) {

        // ======================
        // 1) נתיבי הקבצים
        // ======================
        // קובץ המקור (3000 מילים)
        String inputFilePath = "rec\\worlds\\3000_most_common_words_in_English_clean.txt";

        // קבצי הפלט (5 שיעורים)
        String lesson1Path = "rec\\worlds\\lesson1.txt";
        String lesson2Path = "rec\\worlds\\lesson2.txt";
        String lesson3Path = "rec\\worlds\\lesson3.txt";
        String lesson4Path = "rec\\worlds\\lesson4.txt";
        String lesson5Path = "rec\\worlds\\lesson5.txt";

        // ======================
        // 2) קריאת הקובץ לרשימה
        // ======================
        List<String> allWords = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(inputFilePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                // מנקה רווחים בתחילת/סוף שורה
                line = line.trim();
                if (!line.isEmpty()) {
                    allWords.add(line);
                }
            }
        } catch (IOException e) {
            System.err.println("שגיאה בקריאת הקובץ: " + e.getMessage());
            return;
        }

        // בדיקה אם באמת יש 3000 מילים
        if (allWords.size() != 3000) {
            System.err.println("אזהרה: הקובץ לא מכיל בדיוק 3000 מילים! (נמצאו " + allWords.size() + ")");
            // כאן אפשר להחליט אם לצאת או להמשיך בכל זאת
            // return;
        }

        // ======================
        // 3) מיון מילים לפי אורך
        // ======================
        // נמיין קודם כל מהקצרה לארוכה:
        allWords.sort(Comparator.comparingInt(String::length));

        // עכשיו נאסוף מילים למבנה של מפה (אורך -> רשימת מילים)
        Map<Integer, List<String>> lengthToWordsMap = new LinkedHashMap<>();
        for (String w : allWords) {
            int len = w.length();
            lengthToWordsMap.computeIfAbsent(len, k -> new ArrayList<>()).add(w);
        }

        // ======================
        // 4) הכנת מבנה נתונים לשיעורים
        // ======================
        // רשימה לכל שיעור, כל אחד אמור להכיל 600 מילים בסוף
        List<String> lesson1 = new ArrayList<>(600);
        List<String> lesson2 = new ArrayList<>(600);
        List<String> lesson3 = new ArrayList<>(600);
        List<String> lesson4 = new ArrayList<>(600);
        List<String> lesson5 = new ArrayList<>(600);

        // מערך עם רמת המילוי שנותרה בכל שיעור
        int[] capacity = {600, 600, 600, 600, 600};

        // כדי שיהיה נוח לגשת אליהן לפי אינדקס בלולאה
        List<List<String>> lessons = new ArrayList<>();
        lessons.add(lesson1);
        lessons.add(lesson2);
        lessons.add(lesson3);
        lessons.add(lesson4);
        lessons.add(lesson5);

        // ======================
        // 5) חלוקה אקראית בכל אורך
        // ======================
        // נלך לפי הסדר (מהאורך הקטן לגדול), ונפזר לכל שיעור עד שהוא מתמלא, 
        // ואז עוברים לשיעור הבא
        for (Map.Entry<Integer, List<String>> entry : lengthToWordsMap.entrySet()) {
            List<String> sameLengthWords = entry.getValue();
            // נערבב (shuffle) את המילים באותו אורך
            Collections.shuffle(sameLengthWords);

            // נפיץ בין השיעורים לפי המקום שנותר
            int i = 0; // אינדקס של המילה באורך הנוכחי
            while (i < sameLengthWords.size()) {
                // מחפשים את השיעור הראשון שיש בו מקום
                int lessonIndex = findFirstAvailableLesson(capacity);
                // אם -1 פירושו שכבר אין שיעור פנוי (לא סביר כי סה"כ 3000 מילים)
                if (lessonIndex == -1) {
                    System.err.println("אין מקום בשיעורים! משהו השתבש בחישוב החלוקה.");
                    break;
                }

                int canTake = capacity[lessonIndex]; // כמה מילים אפשר עוד להכניס לשיעור הזה
                int leftInGroup = sameLengthWords.size() - i; // כמה מילים נשארו מהאורך הנוכחי

                // נכניס את מספר המילים המינימלי (או עד סוף הקבוצה, או עד גמר הקיבולת)
                int wordsToTake = Math.min(canTake, leftInGroup);

                // נוציא את אותה פרוסה מהרשימה
                List<String> portion = sameLengthWords.subList(i, i + wordsToTake);

                // נוסיף אותה לשיעור
                lessons.get(lessonIndex).addAll(portion);

                // נעדכן אינדקס וקיבולת
                i += wordsToTake;
                capacity[lessonIndex] -= wordsToTake;
            }
        }

        // אפשר לוודא שבסוף באמת כל שיעור מכיל 600 מילים
        for (int j = 0; j < 5; j++) {
            if (lessons.get(j).size() != 600) {
                System.err.println("אזהרה: lesson " + (j + 1) + " מכיל " + lessons.get(j).size() + " מילים במקום 600.");
            }
        }

        // ======================
        // 6) כתיבה לקבצים
        // ======================
        try (
            BufferedWriter bw1 = new BufferedWriter(new FileWriter(lesson1Path));
            BufferedWriter bw2 = new BufferedWriter(new FileWriter(lesson2Path));
            BufferedWriter bw3 = new BufferedWriter(new FileWriter(lesson3Path));
            BufferedWriter bw4 = new BufferedWriter(new FileWriter(lesson4Path));
            BufferedWriter bw5 = new BufferedWriter(new FileWriter(lesson5Path))
        ) {
            // כותבים את רשימות המילים כפי שהתחלקו
            writeListToFile(lesson1, bw1);
            writeListToFile(lesson2, bw2);
            writeListToFile(lesson3, bw3);
            writeListToFile(lesson4, bw4);
            writeListToFile(lesson5, bw5);

            System.out.println("הקבצים lesson1.txt – lesson5.txt נוצרו בהצלחה!");
        } catch (IOException e) {
            System.err.println("שגיאה בכתיבת הקבצים: " + e.getMessage());
        }

    }

    /**
     * מחפש את האינדקס של השיעור הראשון שבו נותר מקום (capacity>0).
     * אם אין מקום, מחזיר -1.
     */
    private static int findFirstAvailableLesson(int[] capacity) {
        for (int i = 0; i < capacity.length; i++) {
            if (capacity[i] > 0) {
                return i;
            }
        }
        return -1;
    }

    /**
     * פונקציה עזר לכתיבת רשימת מחרוזות ל-BufferedWriter (שורה לכל מחרוזת).
     */
    private static void writeListToFile(List<String> list, BufferedWriter bw) throws IOException {
        for (String word : list) {
            bw.write(word);
            bw.newLine();
        }
    }
}
