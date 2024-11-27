using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.IO;
using System;
using System.Text;

[System.Serializable]
public class ServerResponse
{
    public string user_input;
    public string response_text;
    public string animation;
    public string audio;
}

public class AudioRecorder : MonoBehaviour
{
    [Header("Server Configuration")]
    [SerializeField] private string serverUrl = "http://64.227.183.151:8000/process";
    [SerializeField] private int maxRecordingTime = 10;
    [SerializeField] private int sampleRate = 44100;

    [Header("References")]
    [SerializeField] private AnimationController animationController;

    [Header("Debug Options")]
    [SerializeField] private bool saveDebugFiles = true;
    [SerializeField] private bool logDebugInfo = true;

    private AudioClip audioClip;
    private string microphone;
    private bool isRecording = false;
    private AudioSource audioSource;
    private byte[] recordedAudioData;

    // Events for different response components
    public event Action<string> OnUserInputReceived;
    public event Action<string> OnResponseTextReceived;
    public event Action<string> OnAnimationReceived;
    public event Action OnAudioPlaybackStarted;
    public event Action<string> OnError;

    private void Awake()
    {
        InitializeAudioSource();
    }

    private void Start()
    {
        if (animationController == null)
        {
            animationController = FindObjectOfType<AnimationController>();
            if (animationController == null)
            {
                LogError("AnimationController not found in the scene! Please assign it in the inspector or ensure it exists in the scene.");
            }
            else
            {
                LogDebug("AnimationController found and connected successfully.");
            }
        }
    }

    private void InitializeAudioSource()
    {
        audioSource = GetComponent<AudioSource>();
        if (audioSource == null)
        {
            audioSource = gameObject.AddComponent<AudioSource>();
        }
        LogDebug("AudioSource initialized");
    }

    public void StartRecordingWrapper()
    {
        LogDebug("StartRecordingWrapper called");
        if (isRecording)
        {
            LogError("Recording is already in progress");
            return;
        }
        StartRecording();
    }

    public void StopRecordingWrapper()
    {
        LogDebug("StopRecordingWrapper called");
        if (!isRecording)
        {
            LogError("No recording in progress");
            return;
        }
        StopRecording();
        SendRecordingWrapper();
    }

    private void StartRecording()
    {
        try
        {
            LogDebug("Attempting to start recording");
            if (Microphone.devices.Length == 0)
            {
                throw new System.Exception("No microphone detected!");
            }

            microphone = Microphone.devices[0];
            audioClip = Microphone.Start(microphone, false, maxRecordingTime, sampleRate);

            if (audioClip == null)
            {
                throw new System.Exception("Failed to start microphone recording");
            }

            isRecording = true;
            LogDebug("Recording started...");
        }
        catch (System.Exception e)
        {
            LogError($"Error starting recording: {e.Message}");
        }
    }

    private void StopRecording()
    {
        LogDebug("Stopping recording");
        try
        {
            Microphone.End(microphone);
            isRecording = false;
            LogDebug("Recording stopped");

            if (audioClip != null)
            {
                recordedAudioData = WavUtility.FromAudioClip(audioClip);
                if (recordedAudioData == null || recordedAudioData.Length == 0)
                {
                    throw new System.Exception("Failed to convert audio clip to WAV format");
                }
                LogDebug($"Audio data size: {recordedAudioData.Length} bytes");
            }
            else
            {
                throw new System.Exception("Audio clip is null");
            }
        }
        catch (System.Exception e)
        {
            LogError($"Error stopping recording: {e.Message}");
        }
    }

    private void SendRecordingWrapper()
    {
        LogDebug("SendRecordingWrapper called");
        if (recordedAudioData == null || recordedAudioData.Length == 0)
        {
            LogError("No recorded audio data to send");
            return;
        }
        StartCoroutine(SendAudioData(recordedAudioData));
    }

    private IEnumerator SendAudioData(byte[] audioData)
    {
        LogDebug("Sending audio data to server");
        WWWForm form = new WWWForm();
        form.AddBinaryData("audio", audioData, "audio.wav", "audio/wav");

        using (UnityWebRequest request = UnityWebRequest.Post(serverUrl, form))
        {
            request.timeout = 30; // Increased timeout for processing

            LogDebug($"Sending request to {serverUrl}");
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                LogDebug("Audio data sent successfully");
                ProcessServerResponse(request.downloadHandler.text);
            }
            else
            {
                LogError($"Error sending audio: {request.error}\nResponse Code: {request.responseCode} - {request.downloadHandler.text}");
            }
        }
    }

    private void ProcessServerResponse(string jsonResponse)
    {
        LogDebug("Processing server response");
        try
        {
            LogDebug($"Raw server response: {jsonResponse}");
            ServerResponse response = JsonUtility.FromJson<ServerResponse>(jsonResponse);

            // Handle user input
            if (!string.IsNullOrEmpty(response.user_input))
            {
                LogDebug($"Received user input: {response.user_input}");
                OnUserInputReceived?.Invoke(response.user_input);
            }

            // Handle response text
            if (!string.IsNullOrEmpty(response.response_text))
            {
                LogDebug($"Received response text: {response.response_text}");
                OnResponseTextReceived?.Invoke(response.response_text);
            }

            // Handle animation
            if (!string.IsNullOrEmpty(response.animation))
            {
                LogDebug($"Received animation command: {response.animation}");
                animationController.HandleResponseAnimation(response.animation);
            }

            // Handle audio
            if (!string.IsNullOrEmpty(response.audio))
            {
                LogDebug("Received audio data from server");
                byte[] audioData = Convert.FromBase64String(response.audio);
                if (saveDebugFiles)
                {
                    SaveReceivedAudio(audioData);
                }
                PlayWavAudio(audioData);
            }
        }
        catch (System.Exception e)
        {
            LogError($"Error processing server response: {e.Message}");
        }
    }

    private void PlayWavAudio(byte[] wavData)
    {
        LogDebug("Attempting to play received audio");
        try
        {
            // Convert WAV byte array to AudioClip
            AudioClip clip = WavUtility.ToAudioClip(wavData);

            if (clip == null)
            {
                throw new System.Exception("Failed to convert WAV data to AudioClip");
            }

            audioSource.clip = clip;
            audioSource.Play();
            OnAudioPlaybackStarted?.Invoke();
            LogDebug("Playing received audio");
        }
        catch (System.Exception e)
        {
            LogError($"Error playing WAV audio: {e.Message}");
        }
    }

    private void SaveReceivedAudio(byte[] audioData)
    {
        try
        {
            string path = Path.Combine(Application.persistentDataPath, $"received_audio_{DateTime.Now:yyyyMMdd_HHmmss}.wav");
            File.WriteAllBytes(path, audioData);
            LogDebug($"Received audio saved to: {path}");
        }
        catch (System.Exception e)
        {
            LogError($"Error saving audio file: {e.Message}");
        }
    }

    private void LogDebug(string message)
    {
        if (logDebugInfo)
        {
            Debug.Log($"[AudioProcessor] {message}");
        }
    }

    private void LogError(string message)
    {
        Debug.LogError($"[AudioProcessor] {message}");
        OnError?.Invoke(message);
    }
}
