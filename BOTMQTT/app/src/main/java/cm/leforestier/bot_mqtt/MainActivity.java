package cm.leforestier.bot_mqtt;

import android.os.MessageQueue;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.io.UnsupportedEncodingException;

public class MainActivity extends AppCompatActivity {
// MPAndroidChart Documentation: https://weeklycoding.com/mpandroidchart-documentation/
    final String TAG = MainActivity.class.getSimpleName();
    String topicMsg = "strom/verbrauch";
    byte[] encodeMsg = new byte[0];

    String server = "tcp://192.168.178.28:1883"; // wird geaendert
    String clientID = "Andoid-RUPH";
    MqttClient mqttClient;
    MqttAndroidClient androidClient;
    TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = (TextView) findViewById(R.id.message_id);
        //mqttClient = createClient(server,clientID);
        String clientId = MqttClient.generateClientId();

             androidClient = new MqttAndroidClient(this.getApplicationContext(), server,
                        clientId);


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
                textView.setText(new String(message.getPayload()));
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
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

                        textView.setText(new String(message.getPayload()));
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
}
