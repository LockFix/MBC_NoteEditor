using UnityEngine;
using System.Collections.Generic;
using System;
public class jsoner
{
    [Serializable]
    public class Wrapper<T>
    {
        public List<T> notes;
    }

    public static string ToJson<T>(List<T> list) //리스트를 json 으로
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.notes = list;
        return JsonUtility.ToJson(wrapper);
    }
}
