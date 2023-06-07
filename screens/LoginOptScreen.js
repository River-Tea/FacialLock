import { StyleSheet, Text, View, TouchableOpacity } from 'react-native'
import React from 'react'


const LoginOptScreen = ({ navigation }) => {
    const handleNaviLogin = () => {
        navigation.navigate("Login")
    }
    const handleNaviLoginFace = () => {
        navigation.navigate("LoginFace")
    }
    return (
        <View style={styles.container}>
            <Text style={styles.title}>LoginOptScreen</Text>
            <TouchableOpacity
                style={styles.button}
                onPress={handleNaviLogin}>
                <Text style={styles.buttonText}>Login by password</Text>
            </TouchableOpacity>
            <TouchableOpacity
                style={styles.button}
                onPress={handleNaviLoginFace}>
                <Text style={styles.buttonText}>Lagin by Face</Text>
            </TouchableOpacity>
        </View>
    )
}

export default LoginOptScreen

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