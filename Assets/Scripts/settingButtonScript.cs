using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.InputSystem;

/*
    ***세팅에 관한 모든 것을 처리하는 스크립트***
*/

public class settingButtonScript : MonoBehaviour
{
    public GameObject settingPanel;
    public GameObject bindingOverlay;

    public AudioSource audioSource;

    public TMP_Text firstKey;
    public TMP_Text secondKey;
    public TMP_Text thirdKey;
    public TMP_Text fourthKey;
    public TMP_Text keyGuide1;
    public TMP_Text keyGuide2;
    public TMP_Text keyGuide3;
    public TMP_Text keyGuide4;

    public TMP_Text volumeText;

    public Slider volumeBar;

    public InputActionAsset inputActions;

    public TMP_Dropdown modeDropDown;

    public static short MODE; //0 : make_note, 1 : edit_note

    void Awake()
    { //상태 초기화
        MODE = (short)modeDropDown.GetComponent<TMP_Dropdown>().value;
        GetComponent<UnityEngine.UI.Button>().interactable = false;

        if (!PlayerPrefs.HasKey("Volume")) PlayerPrefs.SetInt("Volume", 100);
        PlayerPrefs.Save();
        Debug.Log("settingButtonScript.cs의 Awake 실행됨");
        GetComponent<UnityEngine.UI.Button>().interactable = true;
    }

    public void onSettingButtonClick()
    { //설정 버튼을 누르면
        Debug.Log("onSettingButtonClick 메서드 호출");
        string key1 = getStringFromAction("firstKey");
        string key2 = getStringFromAction("secondKey");
        string key3 = getStringFromAction("thirdKey");
        string key4 = getStringFromAction("fourthKey");

        int volume = PlayerPrefs.GetInt("Volume");

        firstKey.text = key1;
        secondKey.text = key2;
        thirdKey.text = key3;
        fourthKey.text = key4;

        volumeBar.value = volume;
        settingPanel.SetActive(true);
    }

    public void onExitButtonClick()
    { //X버튼을 누르면
        settingPanel.SetActive(false);
    }

    public void onVolumeChanged(float value)
    { //사용자가 음량을 조절하면
        volumeText.text = value.ToString();

        audioSource.volume = value / 100;
        PlayerPrefs.SetInt("Volume", (int)value);
        PlayerPrefs.Save();
    }

    public void onFirstKeyChangeButtonClick()
    { //1키 변경 버튼 누르면
        InputAction action = inputActions.FindAction("firstKey");
        bindingOverlay.SetActive(true);

        action.PerformInteractiveRebinding().WithControlsExcluding("<Mouse>").OnMatchWaitForAnother(0.1f).OnComplete(operation =>
        {
            string temp = action.GetBindingDisplayString(action.GetBindingIndexForControl(action.controls[0]));
            if (!(firstKey.text == temp || secondKey.text == temp || thirdKey.text == temp || fourthKey.text == temp))
            {
                PlayerPrefs.SetString("key-bind", inputActions.SaveBindingOverridesAsJson());
                PlayerPrefs.Save();
                firstKey.text = temp;
                keyGuide1.text = temp;

                Debug.Log("키 바인딩 : fisrtKey + " + temp);
            }
            operation.Dispose();
            bindingOverlay.SetActive(false);
        }).Start();
    }

    public void onSecondKeyChangeButtonClick()
    { //2키 변경 버튼 누르면
        InputAction action = inputActions.FindAction("secondKey");
        bindingOverlay.SetActive(true);

        action.PerformInteractiveRebinding().WithControlsExcluding("<Mouse>").OnMatchWaitForAnother(0.1f).OnComplete(operation =>
        {
            string temp = action.GetBindingDisplayString(action.GetBindingIndexForControl(action.controls[0]));
            if (!(secondKey.text == temp || firstKey.text == temp || thirdKey.text == temp || fourthKey.text == temp))
            {
                PlayerPrefs.SetString("key-bind", inputActions.SaveBindingOverridesAsJson());
                PlayerPrefs.Save();
                secondKey.text = temp;
                keyGuide2.text = temp;

                Debug.Log("키 바인딩 : secondKey + " + temp);
            }
            operation.Dispose();
            bindingOverlay.SetActive(false);
        }).Start();
    }

    public void onThirdKeyChangeButtonClick()
    { //3키 변경 버튼 누르면
        InputAction action = inputActions.FindAction("thirdKey");
        bindingOverlay.SetActive(true);

        action.PerformInteractiveRebinding().WithControlsExcluding("<Mouse>").OnMatchWaitForAnother(0.1f).OnComplete(operation =>
        {
            string temp = action.GetBindingDisplayString(action.GetBindingIndexForControl(action.controls[0]));
            if (!(thirdKey.text == temp || firstKey.text == temp || secondKey.text == temp || fourthKey.text == temp))
            {
                PlayerPrefs.SetString("key-bind", inputActions.SaveBindingOverridesAsJson());
                PlayerPrefs.Save();
                thirdKey.text = temp;
                keyGuide3.text = temp;

                Debug.Log("키 바인딩 : thirdKey + " + temp);
            }
            operation.Dispose();
            bindingOverlay.SetActive(false);
        }).Start();
    }

    public void onFourthKeyChangeButtonClick()
    { //4키 변경 버튼 누르면
        InputAction action = inputActions.FindAction("fourthKey");
        bindingOverlay.SetActive(true);

        action.PerformInteractiveRebinding().WithControlsExcluding("<Mouse>").OnMatchWaitForAnother(0.1f).OnComplete(operation =>
        {
            string temp = action.GetBindingDisplayString(action.GetBindingIndexForControl(action.controls[0]));
            if (!(fourthKey.text == temp || firstKey.text == temp || secondKey.text == temp || thirdKey.text == temp))
            {
                PlayerPrefs.SetString("key-bind", inputActions.SaveBindingOverridesAsJson());
                PlayerPrefs.Save();
                fourthKey.text = temp;
                keyGuide4.text = temp;

                Debug.Log("키 바인딩 : fourthKey + " + temp);
            }
            operation.Dispose();
            bindingOverlay.SetActive(false);
        }).Start();
    }

    public string getStringFromAction(string actionName)
    {
        InputAction action = inputActions.FindAction(actionName);
        return action.GetBindingDisplayString(action.GetBindingIndexForControl(action.controls[0]));
    }

    public void onModeChanged()
    {
        MODE = (short)modeDropDown.GetComponent<TMP_Dropdown>().value;
    }
}