package cm.leforestier.bot_mqtt;

import android.annotation.SuppressLint;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.formatter.IAxisValueFormatter;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;
import com.github.mikephil.charting.utils.ColorTemplate;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import warning_model.Warning;
import warning_model.WarningManager;

import java.io.UnsupportedEncodingException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {
// MPAndroidChart Documentation: https://weeklycoding.com/mpandroidchart-documentation/
// Exemple 12 : https://www.programcreek.com/java-api-examples/?api=com.github.mikephil.charting.formatter.IAxisValueFormatter
    private final String TAG = MainActivity.class.getSimpleName();

    private String topicMsg = "strom/bot";
    private byte[] encodeMsg = new byte[0];

    private String server = "tcp://192.168.178.28:1883"; // wird geaendert
    private String clientID = "Android-PHONE-NEX05";
    private MqttClient mqttClient;
    private MqttAndroidClient androidClient;

    private TextView msg_tv;
    private TextView date_tv;
    private TextView hour_tv;

    private LineChart graph;
    private EditText tmp_tv;
    private List<Entry> entries = new ArrayList<Entry>();
    private LineDataSet dataSet;
    private ArrayList<ILineDataSet> iLineDataSets;
    private LineData lineData;

    @SuppressLint("SimpleDateFormat")
    private SimpleDateFormat sdf = new SimpleDateFormat("dd MMM YYYY");

    BOTMQTTDB helper;
    SQLiteDatabase database;
    WarningManager manager = new WarningManager();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        onInitializedViews();

        //onWriting(v);
        //onRead();
        //onCreateAndroidClientMQTT();
    }

    private void subscr(String top, int qos){

            try {
                if(androidClient.isConnected()){
                final IMqttToken mqttToken = androidClient.subscribe(top,qos);
                Log.d(TAG,"Client : "+ androidClient +" subscribes to: "+ top);

                // must do a call back
                mqttToken.setActionCallback(new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        // set Text view 2
                        Log.d(TAG,"SUBSCRIPTION SUCCESS ");

                        //textView.setText("chai pas koi prendre");
                    }

                    @Override
                    public void onFailure(IMqttToken asyncActionToken, Throwable exception) {

                    }
                });

                androidClient.setCallback(new MqttCallback() {
                    @Override
                    public void connectionLost(Throwable cause) {

                    }

                    @Override
                    public void messageArrived(String topic, MqttMessage message) throws Exception {
                        Log.d(TAG,"Encoded MSG: "+ message);
                        Toast.makeText(getBaseContext(),new String(message.getPayload())+"  bekommen",Toast.LENGTH_LONG);

                        msg_tv.setText(new String(message.getPayload()));
                    }

                    @Override
                    public void deliveryComplete(IMqttDeliveryToken token) {

                    }
                });
            }
        }catch (MqttException e){e.printStackTrace();}

    }
    public void publishIntoStrom(View view) {
        try {
            String msg = "Ohayo kosalimasu";
            encodeMsg = msg.getBytes("UTF-8");
            MqttMessage mqttMessage = new MqttMessage(encodeMsg);
            Log.d(TAG,"Encoded MSG: "+ encodeMsg);
            androidClient.publish(topicMsg,mqttMessage);
            Toast.makeText(getBaseContext(),new String(msg)+"  published",Toast.LENGTH_LONG);
        }catch (UnsupportedEncodingException | MqttException e){e.printStackTrace();}
    }

    private MqttClient createClient(String url, String id){
        MqttClient mqttClientTmp = null;
        try{
            mqttClientTmp = new MqttClient(url,id);

        }catch (MqttException e){e.printStackTrace();}
        return mqttClientTmp;
    }

    // Graph
    private void onInitializedViews(){
        msg_tv = (TextView) findViewById(R.id.message_id);
        date_tv = (TextView) findViewById(R.id.date_val_id);
        hour_tv = (TextView) findViewById(R.id.hour_val_id);
        tmp_tv = (EditText) findViewById(R.id.tmp_id);
        graph = (LineChart) findViewById(R.id.diag_id);

        helper = new BOTMQTTDB(this);
        database = helper.getWritableDatabase();
        Log.d(TAG, "Views are initialized");

        onSettingGraph(graph);
        entries.add(new Entry(0.0f, 0.0f)); // add values to an  entry
        entries.add(new Entry(4.0f, 9.0f));
        dataSet = new LineDataSet(entries, "Stromverbauch");

        iLineDataSets = new ArrayList<>();
        iLineDataSets.add(dataSet);
        lineData = new LineData(iLineDataSets);

        graph.setData(lineData);
    }

    private void onCreateAndroidClientMQTT(){
        mqttClient = createClient(server,clientID);
        //String clientId = MqttClient.generateClientId();

        androidClient = new MqttAndroidClient(this.getApplicationContext(), server,
                clientID);


        try {
            IMqttToken token = androidClient.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    // We are connected
                    Log.d(TAG, "onSuccess");
                    Toast.makeText(getApplicationContext(),"CONNECTED",Toast.LENGTH_LONG);

                    subscr(topicMsg,0);
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    // Something went wrong e.g. connection timeout or firewall problems
                    Log.d(TAG, "onFailure");

                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }

        // set callback is important but why?
        androidClient.setCallback(new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {

            }
            // https://stackoverflow.com/questions/45349371/how-to-receive-message-in-mqtt-android
            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                // set text view 1
                Log.d(TAG,"Message original: "+ message+"\n Message Str: "+new String(message.getPayload()));
                Toast.makeText(getApplicationContext(),"Message is arrived: "+new String(message.getPayload()),Toast.LENGTH_LONG);
                subscr(topic,1);
                msg_tv.setText(new String(message.getPayload()));
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }

    private void onWriting(double val){

        long datetime = System.currentTimeMillis();
        helper.onInsertValue(val, datetime);
        Log.d(TAG, "Value: ( "+val+" ) saved in the DB");
    }
    private void onRead(){
        List<Warning> warningList = manager.groupDaily(helper.getWarnings());
        msg_tv.setText(String.valueOf(warningList.get(0).getValue()));
        date_tv.setText(warningList.get(0).getDate());
        hour_tv.setText(warningList.get(0).getTime());

        Log.d(TAG, "LIST CONTENT: "+warningList);

        for (Warning w: warningList) {
            Log.d(TAG, "id: " + w.get_id() + "  Value: " + w.getValue() + " Date: " + w.getDate() + "  Time: " + w.getTime());
        }


    }
    private String convertIncomingTime(long itime){
        int hour = (int) ((itime / 1000) / 3600);
        int minuts = (int) (((itime / 1000) / 60) % 60);
        int seconds = (int) ((itime / 1000) % 60);

        return hour + "h : "+minuts+ "m : "+seconds+"s";
    }

    public void onCOmmand(View view) {
        double v = Double.parseDouble(tmp_tv.getText().toString());
        onWriting(v);
        onRead();
    }

    private void onSettingGraph(LineChart chart){

        // enable scaling and dragging
        chart.setDragEnabled(true);
        chart.setScaleEnabled(true);
        chart.setDrawGridBackground(false);
        /*chart.setHighlightPerDragEnabled(true);

        // get the legend (only possible after setting data)
        Legend legend = chart.getLegend();
        legend.setEnabled(false);

        XAxis xAxis = chart.getXAxis();
        xAxis.setPosition(XAxis.XAxisPosition.TOP_INSIDE);
        //xAxis.setTypeface(mTfLight);
        xAxis.setTextSize(10f);
        xAxis.setTextColor(Color.WHITE);
        xAxis.setDrawAxisLine(false);
        xAxis.setDrawGridLines(true);
        xAxis.setTextColor(Color.rgb(255, 192, 56));
        xAxis.setCenterAxisLabels(true);
        xAxis.setGranularity(1f); */// one hour
        /*xAxis.setValueFormatter(new IAxisValueFormatter() {
            @Override
            public String getFormattedValue(float value, AxisBase axis) {
                return sdf.format(new Date((long) value));
            }
        });
*/
        /*YAxis leftAxis = chart.getAxisLeft();
        leftAxis.setPosition(YAxis.YAxisLabelPosition.INSIDE_CHART);
        //leftAxis.setTypeface(mTfLight);
        leftAxis.setTextColor(ColorTemplate.getHoloBlue());
        leftAxis.setDrawGridLines(true);
        leftAxis.setGranularityEnabled(true);
        leftAxis.setAxisMinimum(0f);
        leftAxis.setAxisMaximum(170f);
        leftAxis.setYOffset(-9f);
        leftAxis.setTextColor(Color.rgb(255, 192, 56));

        YAxis rightAxis = chart.getAxisRight();
        rightAxis.setEnabled(false);*/
    }

    //private void setDataSet()
}
