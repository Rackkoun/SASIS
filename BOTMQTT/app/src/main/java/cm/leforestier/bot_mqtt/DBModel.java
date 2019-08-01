package cm.leforestier.bot_mqtt;
// @author: Ruphus
// Created on 01.08.19 at 07:31

public class DBModel {
    private float stromwert;
    private long datetime;

    public DBModel(){}

    public float getStromwert() {
        return stromwert;
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
}
