package cm.leforestier.bot_mqtt;

import android.annotation.SuppressLint;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Color;
import android.graphics.DashPathEffect;
import android.graphics.drawable.Drawable;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;
import com.github.mikephil.charting.utils.Utils;

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
import java.util.List;
/*
* Modified 09.08.2019 at 14:17
* @author: Ruphus
* sources: MPAndroidChart Documentation: https://weeklycoding.com/mpandroidchart-documentation/
*          https://stackoverflow.com/questions/42909979/mpandroidchart-how-can-i-best-set-the-x-axis-values-as-strings-dates
*          Exemple 12 : https://www.programcreek.com/java-api-examples/?api=com.github.mikephil.charting.formatter.IAxisValueFormatter
*          https://stackoverflow.com/questions/41818963/mpandroidchart-v3-x-x-upgraded-from-2-x-x-labels
*          http://shaoniiuc.com/android/android-line-chart-example/
*          https://github.com/PhilJay/MPAndroidChart/wiki/Modifying-the-Viewport
* */
public class MainActivity extends AppCompatActivity {
//
//
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
    private EditText tmp_tv;

    private LineChart graph;
    private List<Entry> entries;
    private LineDataSet lineDataSet;
    private ArrayList<ILineDataSet> iLineDataSets;
    private List<String> xaxis;
    private LineData lineData;

    @SuppressLint("SimpleDateFormat")
    private SimpleDateFormat sdf = new SimpleDateFormat("dd MMM YYYY");

    BOTMQTTDB helper;
    SQLiteDatabase database;
    WarningManager manager = new WarningManager();

    int inc = 0;
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
        onCreateGraph();
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

        onDraw(warningList);
    }

    private void onDraw(List<Warning> warnings){
        //reset();
        entries.add(new Entry(0.0f, 0.0f)); // add values to an  entry
        xaxis.add("0");
        for(int i = 0; i < warnings.size(); i++){
            entries.add(new Entry((float) (i+1), Double.valueOf(warnings.get(i).getValue()).floatValue()));
            xaxis.add(warnings.get(i).getDate());
        }
        lineDataSet = new LineDataSet(entries, "Stromverbrauch");//add the entries with a legend
        onConfigLineDataSet(lineDataSet);

        iLineDataSets.add(lineDataSet);
        lineData = new LineData(iLineDataSets);
        graph.setData(lineData); // first set data

        graph.setTouchEnabled(true);
        graph.setPinchZoom(true);
                                      // then modified viewport
        graph.getXAxis().setPosition(XAxis.XAxisPosition.TOP);
        graph.getAxisRight().setEnabled(false); // don't show right YAxix
        graph.getXAxis().setDrawAxisLine(false);
        graph.getXAxis().setDrawGridLines(false);
        graph.getXAxis().setCenterAxisLabels(false);

        graph.getXAxis().setTextColor(Color.BLACK);
        graph.getXAxis().setTextSize(11f);
        graph.setDrawBorders(false);

        graph.getDescription().setText("Darstellung nicht erdentlicher Stromverbräuche");

        setGraphViewPort();
        graph.animateXY(1200, 2200);
    }

    private void reset(){
        entries = null;
        lineDataSet = null;
        xaxis = null;
        iLineDataSets = null;

        entries = new ArrayList<>();
        xaxis = new ArrayList<>();
        iLineDataSets = new ArrayList<>();

    }

    private void onCreateGraph(){
        reset();

        List<Warning> warningList = manager.groupDaily(helper.getWarnings());
        msg_tv.setText(String.valueOf(warningList.get(0).getValue()));
        date_tv.setText(warningList.get(0).getDate());
        hour_tv.setText(warningList.get(0).getTime());

        Log.d(TAG, "LIST CONTENT: "+warningList);

        for (Warning w: warningList) {
            Log.d(TAG, "id: " + w.get_id() + "  Value: " + w.getValue() + " Date: " + w.getDate() + "  Time: " + w.getTime());
        }

        onDraw(warningList);

        Log.d(TAG, "GraphData: " + graph.getData() + "  DatasetCount: "+ graph.getData().getDataSetCount() +
                "   Number of ENTRY: " + graph.getData().getEntryCount());
    }

    private void onConfigLineDataSet(LineDataSet set){

        set.setDrawIcons(false);
        set.enableDashedLine(10f, 8f, 1f);
        set.enableDashedHighlightLine(10f, 8f, 1f);
        set.setColor(Color.DKGRAY);
        set.setCircleColor(Color.DKGRAY);
        set.setLineWidth(1f);
        set.setCircleRadius(4f);
        set.setValueTextSize(10f);
        set.setDrawFilled(true);
        set.setFormLineWidth(1f);
        set.setFormLineDashEffect(new DashPathEffect(new float[]{10f, 8f}, 1f));
        set.setFormSize(10f);

           if (Utils.getSDKInt() >= 21){
            Drawable drawable = ContextCompat.getDrawable(this, R.drawable.graph_background);
            lineDataSet.setFillDrawable(drawable);
        }
            else {
            lineDataSet.setFillColor(Color.DKGRAY);
        }
    }

    private void onUpdateGraph(){
            inc = graph.getData().getEntryCount();
        if(graph.getData() != null && graph.getData().getEntryCount() > 0){
            Log.d(TAG, "Number of ENTRY: " + graph.getData().getEntryCount());
            entries.add(new Entry((float) inc, (float) 147.45));
            xaxis.add("2019-08-09");
            lineDataSet.setValues(entries);
            //graph.getXAxis().setValueFormatter(new IndexAxisValueFormatter(xaxis));

            //graph.getXAxis().setAxisMaximum(xaxis.size());
            setGraphViewPort();
            graph.getData().notifyDataChanged();
            graph.notifyDataSetChanged();

            graph.animateY(1200);
            //graph.animate();
            graph.moveViewToX(4);


        }
        inc++;
    }

    public void onCOmmand(View view) {
        //double v = Double.parseDouble(tmp_tv.getText().toString());
        //onWriting(v);
        //onRead();
        onUpdateGraph();
    }

    private void setGraphViewPort(){

        graph.getXAxis().setValueFormatter(new IndexAxisValueFormatter(xaxis));

        graph.getXAxis().setGranularity(1f);
        graph.getXAxis().setGranularityEnabled(true);

        graph.getXAxis().setAvoidFirstLastClipping(true); // to avoid that the last value always appear clipped
        graph.setVisibleXRangeMaximum(2);
    }
}
