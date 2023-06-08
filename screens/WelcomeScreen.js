import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React from 'react'

const WelcomeScreen = ({ navigation }) => {

    const handleWelToRegis = async () => {
        navigation.navigate("Register")
    }

    const handleWelToLogin = async () => {
        navigation.navigate("LoginOption")
    }

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Facial Lock</Text>
            <Image
                style={styles.thumbnail}
                source={require('../assets/welcome_thumb.jpg')}
            />
            <TouchableOpacity
                style={styles.button}
                onPress={handleWelToRegis}>
                <Text style={styles.buttonText}>Create A New User</Text>
            </TouchableOpacity>
            <TouchableOpacity
                style={styles.button}
                onPress={handleWelToLogin}>
                <Text style={styles.buttonText}>Login to Existed User</Text>
            </TouchableOpacity>
        </View>
    )
}

export default WelcomeScreen

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
    thumbnail: {
        marginVertical: 20,
        width: 200,
        height: 200,
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
        marginVertical: 10,
    },
    buttonText: {
        color: '#fff',
        fontWeight: 'bold',
    },
})