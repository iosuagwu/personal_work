package db

import (
	"errors"
	"fmt"

	"gopkg.in/mgo.v2/bson"

	. "goProjects/sp-gia/dormMate-api/models"

	"gopkg.in/mgo.v2"
)

const CONNECTIONSTRING = "127.0.0.1"

type MongoConnection struct {
	originalSession *mgo.Session
}

func NewDBConnection() (conn *MongoConnection) {
	conn = new(MongoConnection)
	conn.createConnection()
	return
}

type dbLogger bool

func (w dbLogger) Output(calldepth int, s string) error {
	fmt.Println(s)
	return nil
}

func (c *MongoConnection) createConnection() (err error) {
	dbl := dbLogger(true)
	mgo.SetLogger(dbl)

	fmt.Println("Creating connection to database...")
	mgo.SetDebug(true)
	c.originalSession, err = mgo.Dial(CONNECTIONSTRING)
	if err == nil {
		fmt.Println("Connection established to database")
		UserCollection := c.originalSession.DB("dormmate").C("user-collection")
		if UserCollection == nil {
			err = errors.New("Collection failed, attempt manually")
		}
		index := mgo.Index{
			Key:    []string{"email", "$text:id"},
			Unique: true,
		}
		UserCollection.EnsureIndex(index)
	} else {
		fmt.Printf("Error occured creating connection: %s", err.Error())
	}
	return
}

func (c *MongoConnection) closeConnection() {
	if c.originalSession != nil {
		c.originalSession.Close()
	}
}

func (c *MongoConnection) getSessionAndCollection() (session *mgo.Session, UserCollection *mgo.Collection, err error) {
	if c.originalSession != nil {
		session = c.originalSession.Copy()
		UserCollection = session.DB("dormmate").C("user-collection")
	} else {
		err = errors.New("no original session found")
	}
	return
}

func (c *MongoConnection) AddUser(id string, email string, password string) (err error) {
	session, UserCollection, err := c.getSessionAndCollection()

	if err == nil {
		defer session.Close()

		err = UserCollection.Insert(
			&UserMappingResp{
				Id:       bson.NewObjectId(),
				EMail:    email,
				Password: password,
			},
		)
		if err != nil {
			if mgo.IsDup(err) {
				err = errors.New("Duplicate exists")
			}
		}
	}
	return
}

func (c *MongoConnection) UpdateUser() (err error) {
	return
}

func (c *MongoConnection) GetSingleUser(email string) (password string) {
	result := UserMappingResp{}

	session, UserCollection, err := c.getSessionAndCollection()
	if err != nil {
		fmt.Printf("Error: %s", err)
	}

	defer session.Close()
	err = UserCollection.Find(bson.M{"EMail": email}).One(&result)
	if err != nil {
		fmt.Printf("Error using Find in mgo: %s", err)
	}
	return result.Password
}

func (c *MongoConnection) GetAllUsers() []UserMappingResp {
	session, UserCollection, err := c.getSessionAndCollection()
	if err != nil {
		fmt.Printf("Error: %s", err)
		return nil
	}

	defer session.Close()

	var allUsers []UserMappingResp

	err = UserCollection.Find(nil).All(&allUsers)

	if err != nil {
		fmt.Printf("Could not retrieve collection. Error: %s", err.Error())
	}
	return allUsers
}
