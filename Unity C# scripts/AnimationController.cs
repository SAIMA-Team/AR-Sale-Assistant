using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimationController : MonoBehaviour
{
    private Animator _animator;

    private void Start()
    {
        // Get the Animator component and log if it's missing
        _animator = GetComponent<Animator>();
        if (_animator == null)
        {
            LogDebug("Animator component not found on the model.");
        }
    }

    public void PlayAnimation(string animationName)
    {
        if (_animator != null)
        {
            // Check if the parameter exists as a trigger in the Animator
            if (HasTriggerParameter(animationName))
            {
                LogDebug($"Playing animation: {animationName}");
                _animator.SetTrigger(animationName);
            }
            else
            {
                LogDebug($"Trigger '{animationName}' does not exist in the Animator.");
            }
        }
        else
        {
            LogDebug("Animator component is missing, cannot play animation.");
        }
    }

    public void HandleResponseAnimation(string responseAnimation)
    {
        // Map the response.animation values to the appropriate animation states
        switch (responseAnimation.ToLower())
        {
            case "wave_animation":
                PlayAnimation("wave_animation");
                break;
            case "bow_animation":
                PlayAnimation("bow_animation");
                break;
            case "goodbye_wave_animation":
                PlayAnimation("goodbye_wave_animation");
                break;
            case "talking_animation":
                PlayAnimation("talking_animation");
                break;
            default:
                PlayAnimation("idle");
                break;
        }
    }

    private void LogDebug(string message)
    {
        Debug.Log($"[AnimationController] {message}");
    }

    // Helper method to check if an Animator parameter exists as a trigger
    private bool HasTriggerParameter(string name)
    {
        foreach (AnimatorControllerParameter param in _animator.parameters)
        {
            if (param.name == name && param.type == AnimatorControllerParameterType.Trigger)
            {
                return true;
            }
        }
        return false;
    }
}
