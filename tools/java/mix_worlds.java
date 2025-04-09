
import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class mix_worlds {

    // נתיבים לקבצי הטקסט:
    String lesson1Path = "rec\\worlds\\lesson1.txt";
    String lesson2Path = "rec\\worlds\\lesson2.txt";
    String lesson3Path = "rec\\worlds\\lesson3.txt";
    String lesson4Path = "rec\\worlds\\lesson4.txt";
    String lesson5Path = "rec\\worlds\\lesson5.txt";

    public static void main(String[] args) {
        mix_worlds mixer = new mix_worlds();

        mixer.shuffleFile(mixer.lesson1Path);
        mixer.shuffleFile(mixer.lesson2Path);
        mixer.shuffleFile(mixer.lesson3Path);
        mixer.shuffleFile(mixer.lesson4Path);
        mixer.shuffleFile(mixer.lesson5Path);

        System.out.println("בוצע ערבוב (Shuffle) לכל קבצי השיעורים!");
    }

    /**
     * מתודה שעושה:
     * 1) קוראת את כל השורות מקובץ
     * 2) מערבבת (Shuffle)
     * 3) כותבת חזרה לקובץ
     */
    private void shuffleFile(String filePath) {
        List<String> lines = readFileToList(filePath);
        Collections.shuffle(lines);
        writeListToFile(lines, filePath);
    }

    /**
     * קורא את כל השורות מקובץ לתוך רשימת מחרוזות.
     */
    private List<String> readFileToList(String filePath) {
        List<String> lines = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                // מורידים רווחים מיותרים
                line = line.trim();
                // אם השורה לא ריקה, נוסיף לרשימה
                if (!line.isEmpty()) {
                    lines.add(line);
                }
            }
        } catch (IOException e) {
            System.err.println("שגיאה בקריאת הקובץ " + filePath + ": " + e.getMessage());
        }
        return lines;
    }

    /**
     * כותב רשימת מחרוזות לקובץ (שורה לכל מחרוזת).
     */
    private void writeListToFile(List<String> lines, String filePath) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(filePath))) {
            for (String line : lines) {
                bw.write(line);
                bw.newLine();
            }
        } catch (IOException e) {
            System.err.println("שגיאה בכתיבת הקובץ " + filePath + ": " + e.getMessage());
        }
    }
}
