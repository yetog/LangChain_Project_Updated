import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Button,
  Image,
  ScrollView,
  StyleSheet,
  Platform,
  TouchableOpacity,
  Alert,
} from 'react-native';

import * as Speech from 'expo-speech';
import * as MediaLibrary from 'expo-media-library';

const BASE_URL = 'http://10.0.0.211:5000';

export default function ChatScreen() {
  const [prompt, setPrompt] = useState('');
  const [responseText, setResponseText] = useState('');
  const [imageBase64, setImageBase64] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  const handleChat = async () => {
    setLoading(true);
    setImageBase64(null);
    try {
      const res = await fetch(`${BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      const output = data?.output || data?.properties?.output || '❌ No response.';
      setResponseText(output);

      setChatHistory(prev => [...prev, { role: 'user', content: prompt }, { role: 'assistant', content: output }]);
    } catch (err) {
      setResponseText('❌ Error fetching chat: ' + err.message);
      console.error(err);
    }
    setLoading(false);
  };

  const handleImage = async () => {
    setLoading(true);
    setResponseText('');
    try {
      const res = await fetch(`${BASE_URL}/image`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      if (data.image_base64) {
        setImageBase64(data.image_base64);
      } else {
        setResponseText('❌ No image returned.');
      }
    } catch (err) {
      setResponseText('❌ Error generating image: ' + err.message);
    }
    setLoading(false);
  };

  const handleVoice = () => {
    Speech.speak("Say your prompt and I’ll fill it in for you.");
    // Later we can swap to true STT API
  };

  const handleSaveImage = async () => {
    if (!imageBase64) return;
    const { status } = await MediaLibrary.requestPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission denied', 'Cannot save image without permission');
      return;
    }

    const uri = `data:image/png;base64,${imageBase64}`;
    const asset = await MediaLibrary.createAssetAsync(uri);
    await MediaLibrary.createAlbumAsync('LangChain', asset, false);
    Alert.alert('✅ Saved', 'Image saved to gallery.');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>LangChain Assistant</Text>

      <TextInput
        style={styles.input}
        placeholder="Enter your prompt..."
        placeholderTextColor="#888"
        onChangeText={setPrompt}
        value={prompt}
        multiline
      />

      <View style={styles.buttonRow}>
        <Button title="💬 Chat" onPress={handleChat} disabled={loading} />
        <Button title="🖼️ Image" onPress={handleImage} disabled={loading} />
        <Button title="🎤 Voice" onPress={handleVoice} disabled={loading} />
      </View>

      {loading && <Text style={styles.loading}>Loading...</Text>}

      {/* 🧠 Context Memory Chat Log */}
      <View style={styles.historyBox}>
        {chatHistory.map((entry, index) => (
          <Text
            key={index}
            style={{
              color: entry.role === 'user' ? '#4cefff' : '#fff',
              fontWeight: entry.role === 'user' ? 'bold' : 'normal',
              marginBottom: 4,
            }}
          >
            {entry.role === 'user' ? '🧍 You' : '🤖 AI'}: {entry.content}
          </Text>
        ))}
      </View>

      {/* Response Box */}
      {responseText.length > 0 && (
        <Text style={styles.response}>{responseText}</Text>
      )}

      {/* Image Preview */}
      {imageBase64 && (
        <>
          <Image
            source={{ uri: `data:image/png;base64,${imageBase64}` }}
            style={styles.image}
            resizeMode="contain"
          />
          <TouchableOpacity style={styles.saveButton} onPress={handleSaveImage}>
            <Text style={styles.saveButtonText}>📥 Save Image</Text>
          </TouchableOpacity>
        </>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    paddingTop: 60,
    alignItems: 'center',
    backgroundColor: '#000',
    flexGrow: 1,
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#fff',
  },
  input: {
    width: '100%',
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 10,
    padding: 12,
    marginBottom: 15,
    minHeight: 80,
    textAlignVertical: 'top',
    color: '#fff',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginBottom: 20,
  },
  loading: {
    marginBottom: 10,
    color: 'gray',
  },
  response: {
    fontSize: 16,
    padding: 10,
    backgroundColor: '#f0f0f0',
    borderRadius: 10,
    marginTop: 10,
    width: '100%',
    color: '#000',
  },
  historyBox: {
    width: '100%',
    padding: 12,
    backgroundColor: '#111',
    borderRadius: 10,
    marginBottom: 10,
  },
  image: {
    marginTop: 20,
    width: 300,
    height: 300,
    borderRadius: 10,
  },
  saveButton: {
    marginTop: 10,
    backgroundColor: '#4cefff',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 8,
  },
  saveButtonText: {
    color: '#000',
    fontWeight: 'bold',
  },
});
