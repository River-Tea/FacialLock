import React, { useEffect, useState } from 'react'
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native'
import { Camera } from 'expo-camera';
import * as Permissions from 'expo-permissions';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const API_BASE_URL = 'http://192.168.1.7:5000';

const LoginFaceScreen = ({ navigation }) => {
    const [username, setUsername] = useState('');
    const [hasPermission, setHasPermission] = useState(null);
    const [camera, setCamera] = useState(null);

    useEffect(() => {
        (async () => {
            const { status } = await Permissions.askAsync(Permissions.CAMERA);
            setHasPermission(status === 'granted');
        })();
    }, []);

    if (hasPermission === null) {
        return <View />;
    }
    if (hasPermission === false) {
        return <Text>No access to camera</Text>;
    }

    const handleLoginFace = async () => {
        if (camera) {
            try {
                const photo = await camera.takePictureAsync({ base64: true });
                const response = await axios.post(`${API_BASE_URL}/api/loginFace`, {
                    username,
                    photo: photo.base64,
                });
                await AsyncStorage.setItem('token', response.data.token);

                console.log(response.data);
                navigation.navigate('Home', { userID: username });
            } catch (error) {
                console.error(error.response.data.error);
            }
        }
    };

    const handleUsernameChange = (text) => {
        setUsername(text);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Registration</Text>
            <TextInput
                style={styles.input}
                placeholder="Username"
                onChangeText={handleUsernameChange} />
            <Camera
                style={{ width: 200, height: 270, marginBottom: 10 }}
                type={Camera.Constants.Type.front}
                ref={(ref) => setCamera(ref)} />
            <TouchableOpacity
                style={styles.button}
                onPress={handleLoginFace}>
                <Text style={styles.buttonText}>Login</Text>
            </TouchableOpacity>
        </View>
    )
}

export default LoginFaceScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    input: {
        width: '80%',
        height: 40,
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 5,
        padding: 10,
        marginBottom: 10,
    },
    button: {
        width: '80%',
        height: 40,
        backgroundColor: '#007BFF',
        borderRadius: 5,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 10,
    },
    buttonText: {
        color: '#fff',
        fontWeight: 'bold',
    },
})