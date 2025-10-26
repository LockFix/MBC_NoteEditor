using System.Collections;
using UnityEngine;
using System.Windows.Forms;
using System.IO;
using UnityEngine.UI;
using TMPro;
using UnityEditor.Build.Content;
using System;
using UnityEngine.Networking;

public enum FileType {MP3 = 0, WAV = 1};

public class fileSelectScript : MonoBehaviour
{
    public static int fileType;
    public static AudioClip audioClip;

    public AudioSource audioSource;
    public GameObject audioFile;
    public GameObject loadingPanel; //로딩패널
    public TMP_Text selectedMusicText; //선택한 음악 파일의 이름을 보여줄 텍스트

    private Slider progressBar; //진행바
    private TMP_Text value; //진행 텍스트
    public void fileLoad()
    {
        progressBar = loadingPanel.GetComponentInChildren<Slider>(); //loadingPanel의 자식 노드인 진행바 가져오기
        value = progressBar.GetComponentsInChildren<TMP_Text>()[0]; //progressBar의 자식 노드인 진행 텍스트 가져오기

        string filePath; //원본 파일 경로
        string savePath; //저장 경로
        OpenFileDialog ofd = new OpenFileDialog();
        ofd.Filter = "음악 파일|*.mp3;*.wav;*.ogg"; //음악 파일 필터링
        ofd.Title = "음악 파일 선택하기"; //파일 선택창 제목 설정
        if (ofd.ShowDialog() == DialogResult.OK)
        { //파일 선택창 띄우고 파일을 선택했다면
            loadingPanel.SetActive(true);
            filePath = ofd.FileName; //선택한 파일의 경로 불러오기
            savePath = Path.Combine(UnityEngine.Application.persistentDataPath, "Music");
            if (!Directory.Exists(savePath)) Directory.CreateDirectory(savePath); //저장 경로가 존재하지 않는다면 폴더 생성
            StartCoroutine(loadFile(filePath, Path.Combine(savePath, Path.GetFileName(filePath))));
        }
    }
    IEnumerator loadFile(string sourcePath, string copyPath)
    {
        progressBar.value = 0; //진행바 초기화
        value.text = "0%"; //진행 텍스트 초기화

        const int bufferSize = 1024 * 1024; //버퍼 크기 1mb
        byte[] buffer = new byte[bufferSize]; //버퍼

        long total = new FileInfo(sourcePath).Length; //원본 음악 파일의 크기
        long copied = 0; //복사한 데이터의 크기

        using (FileStream read = new FileStream(sourcePath, FileMode.Open, FileAccess.Read)) //읽기 권한으로 원본 파일 열기
        using (FileStream write = new FileStream(copyPath, FileMode.Create, FileAccess.Write))
        { //쓰기 권한으로 복사 파일 생성
            int bytes;
            while ((bytes = read.Read(buffer, 0, buffer.Length)) > 0)
            {
                write.Write(buffer, 0, bytes);
                copied += bytes;
                float progress = (float)copied / total;
                progressBar.value = progress;
                value.text = Mathf.RoundToInt(progress * 100) + "%";

                yield return null;
            }
        }
        string fileName = Path.GetFileName(sourcePath);
        fileType = (fileName.Substring(fileName.Length - 4) == ".mp3") ? 0 : 1;
        progressBar.value = 1;
        value.text = "100%";
        selectedMusicText.text = fileName;
        Debug.Log("선택한 파일 : " + fileName);
        StartCoroutine(loadAudio(copyPath));
    }

    IEnumerator loadAudio(string path)
    {
        string url = "file://" + path;

        using(UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(url, (fileType == 0) ? AudioType.MPEG : AudioType.WAV))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success) Debug.LogError("audio loading fail : " + www.error);
            else
            {
                audioClip = DownloadHandlerAudioClip.GetContent(www);
                audioSource.clip = audioClip;
            }
        }

        loadingPanel.SetActive(false);
    }
}
