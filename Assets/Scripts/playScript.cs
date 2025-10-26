using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;

public class playScript : MonoBehaviour
{
    public Sprite pauseImage;
    public Sprite playImage;
    public Button pnpButton;
    public Slider playBar;
    public GameObject forwardButton;
    public GameObject backwardButton;

    private InputActionAsset inputActions;
    private InputAction key1;
    private InputAction key2;
    private InputAction key3;
    private InputAction key4;
    private AudioSource audioSource;

    private int pnpState;
    void Awake()
    {
        inputActions = GetComponent<PlayerInput>().actions;
        key1 = inputActions.FindAction("firstKey");
        key2 = inputActions.FindAction("secondKey");
        key3 = inputActions.FindAction("thirdKey");
        key4 = inputActions.FindAction("fourthKey");

        key1.Disable();
        key2.Disable();
        key3.Disable();
        key4.Disable();

        if (!PlayerPrefs.HasKey("key-bind")) PlayerPrefs.SetString("key-bind", inputActions.SaveBindingOverridesAsJson());
        inputActions.LoadBindingOverridesFromJson(PlayerPrefs.GetString("key-bind"));

        Debug.Log("playerScript.cs의 Awake 실행됨");
        pnpState = 0;
    }

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        audioSource = GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void onPlayButton()
    {
        Debug.Log(settingButtonScript.MODE);

        if (pnpState == 0)
        {
            pnpState = 1;
            audioSource.Play();
            StartCoroutine(progressing());
            pnpButton.GetComponent<Image>().sprite = pauseImage;
        }
        else
        {
            pnpState = 0;
            audioSource.Pause();
            pnpButton.GetComponent<Image>().sprite = playImage;
        }
    }

    public void onForwardButton()
    {
        float foTime = audioSource.time + 10;

        if (foTime > audioSource.clip.length) foTime = audioSource.clip.length;
        audioSource.time = foTime;
    }

    public void onBackwardButton()
    {
        float backTime = audioSource.time - 10;

        if (backTime < 0) backTime = 0;
        audioSource.time = backTime;
    }
    
    IEnumerator progressing()
    {
        while(audioSource.isPlaying)
        {
            playBar.value = audioSource.time;
            yield return null;
        }
    }
}
