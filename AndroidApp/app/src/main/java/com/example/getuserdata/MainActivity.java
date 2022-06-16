package com.example.getuserdata;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Environment;
import android.view.View;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ArrayAdapter;

import java.io.DataInput;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    SensorManager sm = null;
    TextView accel_text = null;
    TextView gyro_txt = null;
    List sensor_list;
    Sensor accelerometer;
    Sensor gyroscope;
    String activity_selected = "";
    List<String> accelerometer_data = new ArrayList<>();
    List<String> gyroscope_data = new ArrayList<>();


    // Gets the array of activities from strings.xml and populates the Spinner with its elements
    public void SetActivitySpinner() {
        Spinner activity_spinner = findViewById(R.id.activity_spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.activities, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        activity_spinner.setAdapter(adapter);
    }

    public void startTracking(View view) {
        Spinner spinner = (Spinner)findViewById(R.id.activity_spinner);
        activity_selected = spinner.getSelectedItem().toString();

        // Get sensors and register listener
        sm = (SensorManager) getSystemService(SENSOR_SERVICE);
        accel_text = findViewById(R.id.accel_text);
        gyro_txt = findViewById(R.id.gyro_text);
        accelerometer = sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        gyroscope = sm.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        sensor_list = sm.getSensorList(Sensor.TYPE_ACCELEROMETER);
        sensor_list = sm.getSensorList(Sensor.TYPE_GYROSCOPE);
        if (sensor_list.size() > 0) {
            sm.registerListener(accelEventListener, accelerometer, SensorManager.SENSOR_DELAY_NORMAL);
            sm.registerListener(gyroListener, gyroscope, SensorManager.SENSOR_DELAY_NORMAL);
        }
        else {
            Toast.makeText(getBaseContext(), "Error: No Accelerometer.", Toast.LENGTH_LONG).show();
        }
    }

    public void stopTracking(View view) {
        // unregister sensor listener
        if (sensor_list.size() > 0) {
            sm.unregisterListener(accelEventListener);
            sm.unregisterListener(gyroListener);
        }

        // Check write permission
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1000);
        }

        Date dateTime = new Date();
        @SuppressLint("SimpleDateFormat") SimpleDateFormat dateFormat = new SimpleDateFormat("dd,MM,yy,hh,mm,ss");
        String dateString = dateFormat.format(dateTime);

        // Write the accelerometer data
        String filename = "Download/" + dateString + "," + activity_selected + ",accelerometer";
        if (!filename.equals("") && !activity_selected.equals("")){
            saveTextAsFile(filename, accelerometer_data);
        }

        // Write the gyroscope data
        String gyro_filename = "Download/" + dateString + ","  + activity_selected + ",gyroscope";
        if (!filename.equals("") && !activity_selected.equals("")){
            saveTextAsFile(gyro_filename, gyroscope_data);
        }

        // Write label
        writeLabelsFile();
    }

    private void saveTextAsFile(String filename, List<String> content) {
        String fileName = filename + ".txt";
        File file = new File(Environment.getExternalStorageDirectory().getAbsolutePath(), fileName);

        try {
            FileWriter fr = new FileWriter(file, false);
            for (int i = 0; i < content.size(); i++) {
                fr.write(content.get(i));
            }
            fr.close();
            Toast.makeText(this, "Saved!", Toast.LENGTH_SHORT).show();
        } catch (IOException e) {
            e.printStackTrace();
            Toast.makeText(this, "Error Saving!", Toast.LENGTH_SHORT).show();
        }
//        try {
//            FileOutputStream fos = new FileOutputStream(file);
//            for (int i = 0; i < content.size(); i++) {
//                fos.write(content.get(i).getBytes());
//            }
//            fos.close();
//            Toast.makeText(this, "Saved!", Toast.LENGTH_SHORT).show();
//        } catch (IOException e) {
//            e.printStackTrace();
//            Toast.makeText(this, "Error Saving!", Toast.LENGTH_SHORT).show();
//        }

    }

    public void writeLabelsFile() {
        String filename = "Download/labels.txt";
        File file = new File(Environment.getExternalStorageDirectory().getAbsolutePath(), filename);
        try {
            FileWriter fr = new FileWriter(file, true);
            fr.write(activity_selected + "\n");
            fr.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case 1000:
                if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(this, "Permission granted!", Toast.LENGTH_SHORT).show();
                }
                else {
                    Toast.makeText(this, "Permission not granted!", Toast.LENGTH_SHORT).show();
                    finish();
                }
        }
    }

    SensorEventListener accelEventListener = new SensorEventListener() {
        @SuppressLint("SetTextI18n")
        @Override
        public void onSensorChanged(SensorEvent event) {
            float[] values = event.values;
            accel_text.setText("x: " + values[0] + "\ny: " + values[1] + "\nz: " + values[2]);

            String accel_data = values[0] + "," + values[1] + "," + values[2] + "\n";
            accelerometer_data.add(accel_data);
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int i) { }
    };

    SensorEventListener gyroListener = new SensorEventListener() {
        @SuppressLint("SetTextI18n")
        @Override
        public void onSensorChanged(SensorEvent sensorEvent) {
            float[] values = sensorEvent.values;
            gyro_txt.setText("x: " + values[0] + "\ny: " + values[1] + "\nz: " + values[2]);
            String gyro_data = values[0] + "," + values[1] + "," + values[2] + "\n";
            gyroscope_data.add(gyro_data);
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int i) {

        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        SetActivitySpinner();
    }

    @Override
    protected void onStop() {
//        if (sensor_list.size() > 0) {
//            sm.unregisterListener(accelEventListener);
//            sm.unregisterListener(gyroListener);
//        }
        super.onStop();
    }
}