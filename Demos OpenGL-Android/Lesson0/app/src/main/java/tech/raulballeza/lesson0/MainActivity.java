package tech.raulballeza.lesson0;

/*
Con algunas modificaciones
https://github.com/googleglass/gdk-apidemo-sample/blob/master/app/src/main/java/com/google/android/glass/sample/apidemo/opengl/CubeRenderer.java
 */

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.opengl.GLSurfaceView;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


public class MainActivity extends Activity {

    private final float TOUCH_SCALE_FACTOR = 180.0f / 320;
    private float previousX;
    private float previousY;

    private GLSurfaceView mGLView;

    private CubeRenderer mRenderer;
    //private CubeRenderer_Mejora1 mRenderer;

    private final Handler mHandler = new Handler();



    @SuppressLint("ClickableViewAccessibility") // Medicina Necesaria
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        //this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

        mGLView = findViewById(R.id.OpenGL1_surfaceView);
        mGLView.setEGLContextClientVersion(2);

        mRenderer = new CubeRenderer();
        ///mRenderer = new CubeRenderer_Mejora1();
        mGLView.setRenderer(mRenderer);

        mGLView.setRenderMode(GLSurfaceView.RENDERMODE_CONTINUOUSLY);

        // Importante Entender la diferencia entre estas dos chivas!!!
        //RENDERMODE_CONTINUOUSLY
        //The renderer is called continuously to re-render the scene.

        //RENDERMODE_WHEN_DIRTY
        //The renderer only renders when the surface is created, or when requestRender() is called.  May be called from any thread
/*

        mGLView.setOnTouchListener(new View.OnTouchListener() {

            @Override
            public boolean onTouch(View view, MotionEvent e) {
                float x = e.getX();
                float y = e.getY();


                Log.d("Purito","Posicion X y Y ["+x+","+y+"]");
                switch (e.getAction()) {
                    case MotionEvent.ACTION_MOVE:
                        float dx = x - previousX;
                        mRenderer.mCubeRotation += dx*mRenderer.CUBE_ROTATION_INCREMENT;

                }
                //mPreviousX = x;
                previousX = x;
                previousY = y;
                return true;
            }

        }); */
    }

    public void onWindowFocusChanged(boolean hasFocus){
        super.onWindowFocusChanged(hasFocus);
        View v = (View) findViewById(R.id.OpenGL1_surfaceView);
        String x = Integer.toString(v.getWidth());
        String y = Integer.toString(v.getHeight());
        //show ImageView width and height
        ((TextView)findViewById(R.id.TV1)).setText("Columnas: "+x+" Filas"+y);
    }
}
