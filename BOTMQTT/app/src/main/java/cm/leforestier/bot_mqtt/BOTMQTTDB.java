package cm.leforestier.bot_mqtt;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

// @author: Ruphus
// Created on 01.08.19 at 07:35
// Source 1: Book: Android der schnelle und einfache Einstieg
// Source 2: https://www.programmierenlernenhq.de/tabelle-in-sqlite-datenbank-erstellen-in-android/

public class BOTMQTTDB extends SQLiteOpenHelper {

    private static final String TAG =BOTMQTTDB.class.getSimpleName();

    private static final String DBNAME ="androidmqtt.db";
    private static final int DBVERSION = 1;
    private SQLiteDatabase db;
    // Konstruktor erforderlich
    public BOTMQTTDB(Context context){
        super(context, DBNAME, null, DBVERSION);
        db = getWritableDatabase();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        try {
            // Tabelle erstellen
            String sql = "CREATE TABLE verbrauch " +
                    "(id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    "stromwert REAL NOT NULL, " +
                    "datetime INTEGER NOT NULL);";
            db.execSQL(sql);
            Log.d(TAG, "DB mit dem Namen "+ getDatabaseName()+ " erzeugt");
        }catch (Exception e){
            Log.e(TAG, "Fehler beim Anlegen der DB: " + e.getMessage());
        }
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {}

    // Datensaetze in der DB schreiben und lesen
    public void onWriteInDB(float wert){}
}
