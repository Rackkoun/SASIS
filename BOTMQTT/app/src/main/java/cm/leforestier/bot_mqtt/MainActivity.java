package cm.leforestier.bot_mqtt;

import android.annotation.SuppressLint;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Color;
import android.graphics.DashPathEffect;
import android.graphics.drawable.Drawable;
import android.os.Build;
import android.os.VibrationEffect;
import android.os.Vibrator;

import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.XAxis;
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
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import warning_model.Warning;
import warning_model.WarningManager;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
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

    private MqttAndroidClient androidClient;

    private TextView msg_tv;
    private TextView date_tv;
    private TextView hour_tv;

    private LineChart graph;
    private List<Entry> entries;
    private LineDataSet lineDataSet;
    private ArrayList<ILineDataSet> iLineDataSets;
    private List<String> xaxis;

    @SuppressLint("SimpleDateFormat")
    private SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
    @SuppressLint("SimpleDateFormat")
    private SimpleDateFormat sdf_time = new SimpleDateFormat("hh:mm:ss");

    private double currentMaxUse = 0;
    BOTMQTTDB helper;
    SQLiteDatabase database;
    WarningManager manager = new WarningManager();

    Vibrator vibrator;

    int inc = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        onInitializedViews();

        onCreateAndroidClientMQTT();
    }

    private void subscr(String top){

            try {
                if(androidClient.isConnected()){
                final IMqttToken mqttToken = androidClient.subscribe(top, 0);
                Log.d(TAG,"Client : "+ androidClient +" subscribes to: "+ top);

                // must do a call back
                mqttToken.setActionCallback(new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        // set Text view 2
                        Log.d(TAG,"SUBSCRIPTION SUCCESS ");
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
                    public void messageArrived(String topic, MqttMessage message){
                        try {
                            Log.d(TAG,"Encoded MSG: "+ message);
                            Toast.makeText(getBaseContext(),new String(message.getPayload())+"  bekommen",Toast.LENGTH_LONG).show();

                            msg_tv.setText(new String(message.getPayload()));
                            onWriting(Double.parseDouble(new String(message.getPayload())));

                        }catch (Exception e){
                            e.printStackTrace();
                        }

                    }

                    @Override
                    public void deliveryComplete(IMqttDeliveryToken token) {

                    }
                });
            }
        }catch (MqttException e){e.printStackTrace();}

    }

    // Graph
    private void onInitializedViews(){
        msg_tv = findViewById(R.id.message_id);
        date_tv = findViewById(R.id.date_val_id);
        hour_tv = findViewById(R.id.hour_val_id);
        graph = findViewById(R.id.diag_id);

        helper = new BOTMQTTDB(this);
        database = helper.getWritableDatabase();

        vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
        Log.d(TAG, "Views are initialized");
        onCreateGraph();
    }

    private void onCreateAndroidClientMQTT(){

        String clientID = "Android-PHONE-NEX05";
        String server = "tcp://192.168.178.20:1883";

        androidClient = new MqttAndroidClient(this.getApplicationContext(), server,
                clientID);

        try {
            IMqttToken token = androidClient.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    // We are connected
                    Log.d(TAG, "onSuccess");
                    Toast.makeText(getApplicationContext(),"CONNECTED",Toast.LENGTH_LONG).show();

                    subscr(topicMsg);
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
    }

    private void onWriting(double val){

        long datetime = System.currentTimeMillis();
        helper.onInsertValue(val, datetime);
        Log.d(TAG, "Value: ( "+val+" ) saved in the DB");

        Warning warning = new Warning(val, datetime);
        warning.setDate(sdf.format(new Date(datetime)));
        warning.setTime(sdf_time.format(new Date(datetime)));

        onUpdateGraph(warning);
    }
    private List<Warning> onRead(){
        List<Warning> warningList = manager.groupDaily(helper.getWarnings());

        if (warningList != null){
            Warning w = manager.getHighestUse(warningList);

            currentMaxUse = w.getValue();

            msg_tv.setText(String.valueOf(w.getValue()));
            date_tv.setText(w.getDate());
            hour_tv.setText(w.getTime());

            Log.d(TAG, "LIST CONTENT: "+warningList);

            for (Warning war: warningList) {
                Log.d(TAG, "id: " + war.get_id() + "  Value: " + war.getValue() + " Date: " + war.getDate() + "  Time: " + war.getTime());
            }
        }
        return warningList;
    }

    private void onDraw(List<Warning> warnings){
        //reset();
        entries.add(new Entry(0.0f, 0.0f)); // add values to an  entry
        xaxis.add("0");

        // add to avoid App-crash
        if (warnings != null && warnings.size() > 0){
            for(int i = 0; i < warnings.size(); i++){
                entries.add(new Entry((float) (i+1), Double.valueOf(warnings.get(i).getValue()).floatValue()));
                xaxis.add(warnings.get(i).getDate());
            }
        }
        lineDataSet = new LineDataSet(entries, "Stromverbrauch");//add the entries with a legend
        onConfigLineDataSet(lineDataSet);

        iLineDataSets.add(lineDataSet);
        LineData lineData = new LineData(iLineDataSets);
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
        onDraw(onRead());

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

    private void onUpdateGraph(Warning warning){
            inc = graph.getData().getEntryCount();
        if(graph.getData() != null && graph.getData().getEntryCount() > 0){
            Log.d(TAG, "Number of ENTRY: " + graph.getData().getEntryCount());
            entries.add(new Entry((float) inc, Double.valueOf(warning.getValue()).floatValue()));
            xaxis.add(warning.getDate());
            if(warning.getValue() > currentMaxUse){
                msg_tv.setText(String.valueOf(warning.getValue()));
                date_tv.setText(warning.getDate());
                hour_tv.setText(warning.getTime());

                if (Build.VERSION.SDK_INT >=26){
                    vibrator.vibrate(VibrationEffect
                            .createOneShot(500, VibrationEffect.DEFAULT_AMPLITUDE));
                }

                //onNotify(warning.getValue());
            }
            lineDataSet.setValues(entries);

            setGraphViewPort(); // actualize Viewport

            graph.getData().notifyDataChanged();
            graph.notifyDataSetChanged();

            graph.animateY(1200);
            //graph.animate();
            graph.moveViewToX(4);


        }
        inc++;
    }

    private void setGraphViewPort(){

        graph.getXAxis().setValueFormatter(new IndexAxisValueFormatter(xaxis));

        graph.getXAxis().setGranularity(1f);
        graph.getXAxis().setGranularityEnabled(true);

        graph.getXAxis().setAvoidFirstLastClipping(true); // to avoid that the last value always appear clipped
        graph.setVisibleXRangeMaximum(2);
    }
}
