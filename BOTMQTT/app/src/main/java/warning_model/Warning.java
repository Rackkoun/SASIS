package warning_model;
/*
* @author: Ruphus
* @date: 07.08.2019 at 19:13
* */
public class Warning {
    private long _id;
    private double value;
    private String date;
    private String time;
    private long datetime;

    public Warning(double value, long datetime) {
        this.value = value;
        this.datetime = datetime;
        _id = -1;
    }

    public long get_id() {
        return _id;
    }

    public void set_id(long _id) {
        this._id = _id;
    }

    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public long getDatetime() {
        return datetime;
    }

    public void setDatetime(long datetime) {
        this.datetime = datetime;
    }
}
