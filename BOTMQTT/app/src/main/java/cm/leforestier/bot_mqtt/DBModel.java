package cm.leforestier.bot_mqtt;
// @author: Ruphus
// Created on 01.08.19 at 07:31

public class DBModel {
    private int _id;
    private float stromwert;
    private long datetime;

    public DBModel(){}

    public DBModel(float stromwert, long datetime){
        this.stromwert = stromwert;
        this.datetime = datetime;
        _id = -1;
    }
    public float getStromwert() {
        return stromwert;
    }

    public int get_id() {
        return _id;
    }

    public long getDatetime() {
        return datetime;
    }

    public void setDatetime(long datetime) {
        this.datetime = datetime;
    }

    public void setStromwert(float stromwert) {
        this.stromwert = stromwert;
    }

    public void set_id(int _id) {
        this._id = _id;
    }
}
