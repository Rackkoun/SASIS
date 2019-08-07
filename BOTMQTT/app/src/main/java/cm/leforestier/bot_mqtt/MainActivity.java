package cm.leforestier.bot_mqtt;

import android.database.sqlite.SQLiteDatabase;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.data.Entry;
import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import warning_model.WarningManager;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
// MPAndroidChart Documentation: https://weeklycoding.com/mpandroidchart-documentation/
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

    List<Entry> entries = new ArrayList<Entry>();

    BOTMQTTDB helper;
    SQLiteDatabase database;
    WarningManager manager = new WarningManager();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        onInitializedViews();
        onCreateAndroidClientMQTT();
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
        graph = (LineChart) findViewById(R.id.diag_id);

        entries.add(new Entry(0.0f, 0.0f)); // add values to an  entry

        helper = new BOTMQTTDB(this);
        database = helper.getWritableDatabase();
        Log.d(TAG, "Views are initialized");
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
}
