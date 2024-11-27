using UnityEngine;
using UnityEngine.Android;

public class PermissionManager : MonoBehaviour
{
    void Start()
    {
        RequestPermissions();
    }

    public void RequestPermissions()
    {
        // Request microphone permission
        if (!Permission.HasUserAuthorizedPermission(Permission.Microphone))
        {
            Permission.RequestUserPermission(Permission.Microphone);
        }

        // Request camera permission for AR
        if (!Permission.HasUserAuthorizedPermission(Permission.Camera))
        {
            Permission.RequestUserPermission(Permission.Camera);
        }

        // Request location permission
        if (!Permission.HasUserAuthorizedPermission(Permission.FineLocation))
        {
            Permission.RequestUserPermission(Permission.FineLocation);
        }
    }

    // Check individual permissions
    public bool HasMicrophonePermission()
    {
        return Permission.HasUserAuthorizedPermission(Permission.Microphone);
    }

    public bool HasInternetConnection()
    {
        return Application.internetReachability != NetworkReachability.NotReachable;
    }

    public bool HasCameraPermission()
    {
        return Permission.HasUserAuthorizedPermission(Permission.Camera);
    }

    public bool HasLocationPermission()
    {
        return Permission.HasUserAuthorizedPermission(Permission.FineLocation);
    }

    // Check if all required permissions are granted
    public bool HasAllRequiredPermissions()
    {
        return HasMicrophonePermission() &&
               HasCameraPermission() &&
               HasLocationPermission() &&
               HasInternetConnection();
    }
}