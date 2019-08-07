package cm.leforestier.bot_mqtt;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;
import warning_model.Warning;

import java.util.ArrayList;
import java.util.List;

// @author: Ruphus
// Created on 01.08.19 at 07:35
// Source 1: Book: Android der schnelle und einfache Einstieg
// Source 2: Project FB4FIT @author Ruphus

public class BOTMQTTDB extends SQLiteOpenHelper {

    private static final String TAG =BOTMQTTDB.class.getSimpleName();

    private static final String DBNAME ="androidmqtt.db";
    private static final int DBVERSION = 1;

    // Datenbanken-Tabelle
    private static final String WARNING_TABLE = "warning";

    // Columns's name
    private static final String _ID = "_id";
    private static final String COLUMN_VALUE = "value";
    private static final String COLUMN_DATETIME = "datetime";

    // drop table
    private static final String DROP_WARNING_TABLE = "DROP TABLE IF EXISTS " + WARNING_TABLE;


    private SQLiteDatabase db;

    // Konstruktor erforderlich
    public BOTMQTTDB(Context context){
        super(context, DBNAME, null, DBVERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        try {
            // Tabelle erstellen
            String sql = "CREATE TABLE " + WARNING_TABLE +
                    "("+ _ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                          COLUMN_VALUE + " REAL NOT NULL, " +
                          COLUMN_DATETIME +" TEXT);";

            db.execSQL(sql);
            Log.d(TAG, "DB mit dem Namen "+ getDatabaseName()+ " erzeugt");
        }catch (Exception e){
            Log.e(TAG, "Fehler beim Anlegen der DB: " + e.getMessage());
        }
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        try {
            db.execSQL(DROP_WARNING_TABLE);

            onCreate(db);
            Log.d(TAG, "DB mit dem Namen "+ getDatabaseName()+ " erzeugt");
        }catch (Exception e){
            Log.e(TAG, "Fehler beim Anlegen der DB: " + e.getMessage());
        }
    }

    // Datensaetze in der DB schreiben und lesen
    public void onInsertValue(double value, long insertedDatetime){

        SQLiteDatabase db = getWritableDatabase();
        db.beginTransaction(); // Besser Werte mit einer Transaktion in der Tabelle einzutragen
        try {
            ContentValues contentValues = new ContentValues();
            contentValues.put(COLUMN_VALUE, value);
            contentValues.put(COLUMN_DATETIME, insertedDatetime);
            long id = db.insert(WARNING_TABLE, null, contentValues);

            db.setTransactionSuccessful(); // dann die Transaktion abschliessen
            Log.d(TAG, "id: " + id + " values " + value + " Datetime: " + insertedDatetime + "\n" +
                    " erfolgreich eingetragen");
        }catch (Exception e){
            Log.d(getClass().getSimpleName(), "Fehler beim Eintragen der Werte: \n"+ e.getMessage());
        }
        finally {
            db.endTransaction();
        }

    }

    // get the list of inserted elements in the database
    public List<Warning> getWarnings(){
        SQLiteDatabase liteDatabase = getReadableDatabase();
        List<Warning> warnings = new ArrayList<>();
        Cursor cursor = liteDatabase.query(WARNING_TABLE,
                null,
                null, null, null, null, null);

        if (cursor.moveToFirst()){
            Log.d(getClass().getSimpleName(), "Elements in List:\n");
            do {
                long id = cursor.getLong(0);
                double value = cursor.getDouble(1);
                long datetime = cursor.getLong(2);
                Warning warning = new Warning(value, datetime);
                warning.set_id(id);
                Log.d(getClass().getSimpleName(),
                        "ID: "+warning.get_id() + "   Max: " + warning.getValue()+ "   Datetime: " + warning.getDatetime());
                warnings.add(warning);

            }while (cursor.moveToNext());
        }
        cursor.close();
        return warnings;
    }

    // Delete Table in the Database
    public void onDeleteWarnings() {
        SQLiteDatabase db = getWritableDatabase();
        db.beginTransaction();

        try {
            db.delete(WARNING_TABLE, null, null);
            db.setTransactionSuccessful();
            Log.d(TAG, "Contain deleted successfully!");
        } catch (Exception e) {
            Log.d(TAG, "Error while deleting Table: " + WARNING_TABLE);
            e.getMessage();
        } finally {
            db.endTransaction();
        }
    }
}
