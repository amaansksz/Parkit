import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Alert, Platform, StatusBar } from "react-native";
import { firestore_DB } from '../../db/firebase';
import { collection, query, where, getDocs } from 'firebase/firestore';
import { Ionicons } from '@expo/vector-icons';

const UserBookings = ({ route, navigation }) => {
  const [bookings, setBookings] = useState([]);
  const { email, name } = route.params;

  useEffect(() => {
    // Fetch bookings data for the specified user
    const fetchBookings = async () => {
      const q = query(
        collection(firestore_DB, 'user_bookings'),
        where('email', '==', email)
      );
      const querySnapshot = await getDocs(q);

      const fetchedBookings = [];
      querySnapshot.forEach((doc) => {
        fetchedBookings.push(doc.data());
      });

      setBookings(fetchedBookings);
    };

    fetchBookings();
  }, []); // Trigger fetchBookings only once on component mount

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.navigate('Home')}>
          <Ionicons name="arrow-back" size={24} color="black" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Your Bookings</Text>
        <View />
      </View>

      {bookings.length === 0 ? (
        <View style={styles.noBookingsContainer}>
          <Text style={styles.noBookingsText}>No bookings done yet</Text>
        </View>
      ) : (
        <View style={styles.tableContainer}>
          <View style={styles.table}>
            <View style={styles.tableHeader}>
              <Text style={styles.headerText}>Licence</Text>
              <Text style={styles.headerText}>Start Time</Text>
              <Text style={styles.headerText}>End Time</Text>
              <Text style={styles.headerText}>Fees</Text>
            </View>
            {bookings.map((booking, index) => (
              <View key={index} style={styles.row}>
                <Text style={styles.rowText}>{booking.plate_no}</Text>
                <Text style={styles.rowText}>{booking.entry_time.toDate().toLocaleString()}</Text>
                <Text style={styles.rowText}>{booking.exit_time.toDate().toLocaleString()}</Text>
                <Text style={styles.rowText}>{booking.fees}</Text>
              </View>
            ))}
          </View>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight + 20 : 0,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  tableContainer: {
    flex: 1,
    justifyContent: 'center',
  },
  table: {
    width: '100%',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    marginBottom: 20,
  },
  tableHeader: {
    flexDirection: 'row',
    backgroundColor: '#f0f0f0',
    paddingVertical: 10,
  },
  headerText: {
    flex: 1,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  row: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderColor: '#ccc',
    paddingVertical: 10,
  },
  rowText: {
    flex: 1,
    textAlign: 'center',
  },
  noBookingsContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  noBookingsText: {
    textAlign: 'center',
    fontSize: 16,
  },
});

export default UserBookings;
