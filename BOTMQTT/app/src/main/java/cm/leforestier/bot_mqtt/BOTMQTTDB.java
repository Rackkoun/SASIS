package cm.leforestier.bot_mqtt;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

// @author: Ruphus
// Created on 01.08.19 at 07:35
// Source: Book: Android der schnelle und einfache Einstieg

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
        // Tabelle erstellen
        String sql = "CREATE TABLE verbrauch " +
                     "(id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                     "stromwert REAL NOT NULL, " +
                     "datetime INTEGER NOT NULL)";
        db.execSQL(sql);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

    }
}
