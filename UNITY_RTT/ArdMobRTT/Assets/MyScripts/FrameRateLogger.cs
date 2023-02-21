/*
by Moritz Wunderwald, 2023
https://github.com/wunderwald/
moritzwunderwald@yahoo.de
*/


using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class FrameRateLogger : MonoBehaviour
{
    private string logFileName = "framerate_log.csv";
    private List<string> logData = new List<string>();
    private float timeElapsed;

    private void Start()
    {
        QualitySettings.vSyncCount = 0;
        Application.targetFrameRate = -1;

        logData.Add("Frame Rate");

        timeElapsed = 0f;
    }

    private void Update()
    {
        float frameRate = 1f / Time.deltaTime;

        logData.Add(frameRate.ToString("0"));

        timeElapsed += Time.deltaTime;

        if (timeElapsed >= 1f)
        {
            timeElapsed = 0f;
        }
    }

    private void OnApplicationQuit()
    {
        string filePath = Application.dataPath + "/" + logFileName;

        StreamWriter writer = new StreamWriter(filePath, false);

        foreach (string line in logData)
        {
            writer.WriteLine(line);
        }

        writer.Flush();
        writer.Close();

    }
}
