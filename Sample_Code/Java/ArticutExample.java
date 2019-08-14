import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;


public class ArticutExample {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        HttpURLConnection urlConnection = null;
        URL url = null;
        try {
            url = new URL("https://api.droidtown.co/Articut/API/");
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod("POST");
            urlConnection.setRequestProperty("Content-Type", "application/json; utf-8");
            urlConnection.setRequestProperty("Accept", "application/json");
            urlConnection.setDoOutput(true);
            urlConnection.setDoInput(true);

            // Articut Parameters
            JSONObject requestJson = new JSONObject();
            requestJson.put("username", "");
            requestJson.put("api_key", "");
            requestJson.put("input_str", "努力才能成功");
            requestJson.put("version", "latest");
            requestJson.put("level", "lv2");

            // Send Request
            OutputStream out = urlConnection.getOutputStream();
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(out));
            bw.write(requestJson.toString());
            bw.flush();
            out.close();
            bw.close();

            if (urlConnection.getResponseCode() == HttpURLConnection.HTTP_OK) {
                InputStream in = urlConnection.getInputStream();
                BufferedReader br = new BufferedReader(new InputStreamReader(in));
                String str = null;
                StringBuffer buffer = new StringBuffer();
                while ((str = br.readLine()) != null) {
                    buffer.append(str);
                }
                in.close();
                br.close();
                JSONObject resultJson = new JSONObject(buffer.toString());
                System.out.println("status: " + resultJson.getBoolean("status"));
                System.out.println("msg: " + resultJson.getString("msg"));
                System.out.println("result_pos: " + resultJson.getJSONArray("result_pos").toString());
                System.out.println("result_segmentation: " + resultJson.getString("result_segmentation"));
                System.out.println("exec_time: " + resultJson.getFloat("exec_time"));
                System.out.println("version: " + resultJson.getString("version"));
                System.out.println("level: " + resultJson.getString("level"));
                System.out.println("word_count_balance: " + resultJson.getInt("word_count_balance"));
            }

            urlConnection.disconnect();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

}
