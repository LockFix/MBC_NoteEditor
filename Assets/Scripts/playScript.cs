using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using TMPro;
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
    public GameObject savedPanel;
    public GameObject logPrefab; //로그 프리팹s
    public Transform content; //로그를 띄울 스크롤뷰의 콘텐츠뷰
    public TMP_Text presentTimeText;
    public Image keyGuide1;
    public Image keyGuide2;
    public Image keyGuide3;
    public Image keyGuide4;
    public TMP_InputField fileNameInputField;

    private InputActionAsset inputActions;
    private InputAction key1;
    private InputAction key2;
    private InputAction key3;
    private InputAction key4;
    private AudioSource audioSource;
    private FileStream fileWriter;
    private string filePath;

    private int pnpState;

    [Serializable]
    public class NoteData //json 출력 파일에 담길 각 노트의 데이터 클래스
    {
        public int direction; //노트 방향
        public float timing; //노트 타이밍
        public NoteData(int direction, float timing)
        {
            this.direction = direction;
            this.timing = timing;
        }
    }

    public List<NoteData> noteDatas;

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

        keyGuide1.GetComponentInChildren<TMP_Text>().text = getStringFromAction("firstKey");
        keyGuide2.GetComponentInChildren<TMP_Text>().text = getStringFromAction("secondKey");
        keyGuide3.GetComponentInChildren<TMP_Text>().text = getStringFromAction("thirdKey");
        keyGuide4.GetComponentInChildren<TMP_Text>().text = getStringFromAction("fourthKey");

        Debug.Log("playerScript.cs의 Awake 실행됨");
        pnpState = 0;
    }

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        audioSource = GetComponent<AudioSource>();
        noteDatas = new List<NoteData>();
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
            if (settingButtonScript.MODE == 0) //플레이
            {
                if (fileSelectScript.isSelectedFolderPath && fileSelectScript.outputFileName != "")
                {
                    noteDatas = new List<NoteData>();
                    fileNameInputField.interactable = false;

                    foreach(Transform child in content) //로그 기록 비우기
                    {
                        Destroy(child.gameObject);
                    }

                    filePath = Path.Combine(fileSelectScript.outputFolderPath, fileSelectScript.outputFileName + ".json"); //출력 파일 json 형식으로 저장
                    fileWriter = new FileStream(filePath, FileMode.Create, FileAccess.Write);

                    playMusic();

                    key1.Enable();
                    key2.Enable();
                    key3.Enable();
                    key4.Enable();
                }
            }
        }
        else if (pnpState == 1) //이어 플레이
        {
            if (settingButtonScript.MODE == 0)
            {
                if (fileSelectScript.isSelectedFolderPath && fileSelectScript.outputFileName != "")
                {
                    fileNameInputField.interactable = false;
                    playMusic();

                    key1.Enable();
                    key2.Enable();
                    key3.Enable();
                    key4.Enable();
                }
            }
        }
        else //일시정지
        {
            pnpState = 1;

            key1.Disable();
            key2.Disable();
            key3.Disable();
            key4.Disable();

            audioSource.Pause();
            pnpButton.GetComponent<Image>().sprite = playImage;
        }
    }

    public void onStopButton() //완전 stop
    {
        fileWriter.Write(Encoding.UTF8.GetBytes(jsoner.ToJson(noteDatas))); //출력 파일 저장
        fileWriter.Close(); //메모리 누수 방지
        savedPanel.SetActive(true);
        fileSelectScript.outputFileName = "";
        fileNameInputField.text = "";

        key1.Disable();
        key2.Disable();
        key3.Disable();
        key4.Disable();

        Debug.Log("Audio stopped");

        audioSource.Stop();
        pnpState = 0;
        playBar.value = 0;
        presentTimeText.text = "00:00:00";
        pnpButton.GetComponent<Image>().sprite = playImage;
        fileNameInputField.interactable = true;
    }

    public void onForwardButton()
    {
        float foTime = audioSource.time + 10;

        if (foTime > audioSource.clip.length) foTime = audioSource.clip.length;
        audioSource.time = foTime;
        if (foTime < 3600)
        {
            presentTimeText.text = ((int)foTime / 60).ToString() + ":" + ((int)foTime % 60).ToString();
        }
        else
        {
            presentTimeText.text = ((int)foTime / 3600).ToString() + ":" + ((int)foTime % 3600 / 60).ToString() + ":" + ((int)foTime % 3600 % 60).ToString();
        }
    }

    public void onBackwardButton()
    {
        float backTime = audioSource.time - 10;

        if (backTime < 0) backTime = 0;
        audioSource.time = backTime;
        if (backTime < 3600)
        {
            presentTimeText.text = ((int)backTime / 60).ToString() + ":" + ((int)backTime % 60).ToString();
        }
        else
        {
            presentTimeText.text = ((int)backTime / 3600).ToString() + ":" + ((int)backTime % 3600 / 60).ToString() + ":" + ((int)backTime % 3600 % 60).ToString();
        }
    }

    private void playMusic()
    {
        pnpState = 2;
        audioSource.Play();
        StartCoroutine(progressing());
        pnpButton.GetComponent<Image>().sprite = pauseImage;
    }

    IEnumerator progressing()
    {
        while (audioSource.isPlaying)
        {
            playBar.value = audioSource.time;
            yield return null;
            if (audioSource.time < 3600)
            {
                presentTimeText.text = ((int)audioSource.time / 60).ToString() + ":" + ((int)audioSource.time % 60).ToString();
            }
            else
            {
                presentTimeText.text = ((int)audioSource.time / 3600).ToString() + ":" + ((int)audioSource.time % 3600 / 60).ToString() + ":" + ((int)audioSource.time % 3600 % 60).ToString();
            }

            yield return null;
        }
        if (audioSource.time == audioSource.clip.length)
        {
            playBar.value = 0;
            presentTimeText.text = "00:00:00";
        }
    }

    public void addNote(int direction) //노트 데이터 추가 메서드
    {
        float timing = audioSource.time;
        NoteData noteData = new NoteData(direction, timing);
        noteDatas.Add(noteData);

        GameObject log = Instantiate(Resources.Load("Prefabs/log", typeof(GameObject)), content) as GameObject;
        log.GetComponentInChildren<Image>().GetComponentInChildren<TMP_Text>().text = JsonUtility.ToJson(noteData);
    }

    //노트 입력 메서드 구현
    public void OnFirstKey()
    {
        addNote(1);
        StartCoroutine(highlightedEffect(keyGuide1));

        Debug.Log("1키 눌림.");
    }

    public void OnSecondKey()
    {
        addNote(2);
        StartCoroutine(highlightedEffect(keyGuide2));

        Debug.Log("2키 눌림.");
    }

    public void OnThirdKey()
    {
        addNote(3);
        StartCoroutine(highlightedEffect(keyGuide3));

        Debug.Log("3키 눌림.");
    }

    public void OnFourthKey()
    {
        addNote(4);
        StartCoroutine(highlightedEffect(keyGuide4));

        Debug.Log("4키 눌림.");
    }

    public void onCheckedSaveingButton()
    {
        savedPanel.SetActive(false);
    }

    public string getStringFromAction(string actionName)
    {
        InputAction action = inputActions.FindAction(actionName);
        return action.GetBindingDisplayString(action.GetBindingIndexForControl(action.controls[0]));
    }
    
    IEnumerator highlightedEffect(Image image)
    {
        image.color = new Color(0.78f, 0.78f, 0.78f, 1);
        yield return new WaitForSeconds(0.1f);
        image.color = new Color(1, 1, 1, 1);
    }
}
