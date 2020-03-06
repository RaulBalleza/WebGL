package com.example.lesson13;

import android.Manifest;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.PixelFormat;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.opengl.GLSurfaceView;
import android.os.AsyncTask;
import android.os.Environment;
//import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.Surface;
import android.widget.FrameLayout;
import android.hardware.Camera;
import android.hardware.Camera.PictureCallback;
import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.core.app.ActivityCompat;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;


//public class MainActivity extends AppCompatActivity   implements  PictureCallback    {
public class MainActivity extends Activity implements PictureCallback {

    private static final int REQUEST_ID_CAMERA_PERMISSION = 100;

    CameraSurfaceView cameraSurfaceView;
    Button shutterButton;
    Button saveFrameBufferButton;

    private GLSurfaceView mGLView;
    private CubeRenderer mRenderer;
    FrameLayout preview;

    private int getRotacion(int rotation) {
        int angle;
        switch (rotation) {
            case Surface.ROTATION_90:
                angle = -90;
                break;
            case Surface.ROTATION_180:
                angle = 180;
                break;
            case Surface.ROTATION_270:
                angle = 90;
                break;
            default:
                angle = 0;
                break;
        }
        return angle;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        askPermissionOnly();

        //this.requestWindowFeature()
        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

        int rotation = getWindowManager().getDefaultDisplay().getRotation();
        TextView TV1 = findViewById(R.id.TV_info);
        TV1.setText("Angulo : " + getRotacion(rotation));

        // set up our preview surface
        preview = (FrameLayout) findViewById(R.id.camera_preview);
        cameraSurfaceView = new CameraSurfaceView(this);
        preview.addView(cameraSurfaceView);


        mRenderer = new CubeRenderer();

        mGLView = findViewById(R.id.OpenGL_preview);
        mGLView.setEGLContextClientVersion(2);
        mGLView.setZOrderOnTop(true);
        mGLView.setEGLConfigChooser(8, 8, 8, 8, 16, 0);
        //mGLView.getHolder().setFormat(PixelFormat.TRANSLUCENT);
        mGLView.getHolder().setFormat(PixelFormat.RGBA_8888);

        mGLView.setRenderer(mRenderer);
        mGLView.setRenderMode(GLSurfaceView.RENDERMODE_CONTINUOUSLY);

        // grab out shutter button so we can reference it later
        shutterButton = (Button) findViewById(R.id.shutter_button);
        shutterButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                takePicture();
            }
        });
    }


    private void takePicture() {
        shutterButton.setEnabled(false);
        cameraSurfaceView.takePicture(this);
    }

    @Override
    public void onPictureTaken(byte[] data, Camera camera) {

        //camera.startPreview();
        //shutterButton.setEnabled(true);

        //new SaveImageTask().execute(data);
        cameraSurfaceView.resetCam();
        new SaveImageTask().execute(data);
        shutterButton.setEnabled(true);


    }

    private class SaveImageTask extends AsyncTask<byte[], Void, String> {

        @Override
        protected String doInBackground(byte[]... data) {
            FileOutputStream outStream = null;
            String imagePath = "";

            // Write to SD Card
            try {
                File sdCard = Environment.getExternalStorageDirectory();
                File dir = new File(sdCard.getAbsolutePath() + "/camtest");
                dir.mkdirs();

                String fileName = String.format("%d.jpg", System.currentTimeMillis());
                File outFile = new File(dir, fileName);

                outStream = new FileOutputStream(outFile);
                outStream.write(data[0]);
                outStream.flush();
                outStream.close();

                // Enviar al servidor !!!
                imagePath = outFile.getAbsolutePath();


                refreshGallery(outFile);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
            }
            return imagePath;
        }

        @Override
        protected void onPostExecute(String result) {
            Toast.makeText(getApplicationContext(), "Se guardo el archivo: " + result, Toast.LENGTH_SHORT).show();

        }


    }


    private void refreshGallery(File file) {
        Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
        mediaScanIntent.setData(Uri.fromFile(file));
        sendBroadcast(mediaScanIntent);
    }

    // Funcionaes de Permisos
    private void askPermissionOnly() {
        this.askPermission(REQUEST_ID_CAMERA_PERMISSION,
                Manifest.permission.CAMERA);
        this.askPermission(REQUEST_ID_CAMERA_PERMISSION,
                Manifest.permission.WRITE_EXTERNAL_STORAGE);
    }

    // With Android Level >= 23, you have to ask the user
    // for permission with device (For example read/write data on the device).
    private boolean askPermission(int requestId, String permissionName) {
        if (android.os.Build.VERSION.SDK_INT >= 23) {
            // Check if we have permission
            int permission = ActivityCompat.checkSelfPermission(this, permissionName);
            if (permission != PackageManager.PERMISSION_GRANTED) {
                // If don't have permission so prompt the user.
                this.requestPermissions(
                        new String[]{permissionName},
                        requestId
                );
                return false;
            }
        }
        return true;
    }

    // When you have the request results
    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {

        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        //
        // Note: If request is cancelled, the result arrays are empty.
        if (grantResults.length > 0) {
            switch (requestCode) {
                case REQUEST_ID_CAMERA_PERMISSION: {
                    if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                        Toast.makeText(getApplicationContext(), "Permission Lectura Concedido!", Toast.LENGTH_SHORT).show();

                    }
                }
            }
        } else {
            Toast.makeText(getApplicationContext(), "Permission Cancelled!", Toast.LENGTH_SHORT).show();
        }
    }

}
