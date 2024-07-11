package models

import (
	"gopkg.in/mgo.v2/bson"
)

type UserMapping struct {
	ID        string   `json:"id" bson:"id"`
	EMail     string   `json:email bson:email`
	Password  string   `json:password bson:password`
	FirstName string   `json:fName bson:fName`
	LastName  string   `json:lName bson:lName`
	Gender    string   `json:gender bson:gender`
	Class     string   `json:class bson:class`
	Hometown  string   `json:hometown bson:hometown`
	Major     string   `json:major bson:major`
	Smoke     bool     `json:smoke bson:smoke`
	Alcohol   bool     `json:alcohol bson:alcohol`
	Snore     bool     `json:snore bson:snore`
	Bio       string   `json:bio bson:bio`
	Bedtime   string   `json:bedtime bson:bedtime`
	Neatness  bool     `json:neatness bson:neatness`
	Likes     []string `json:likes bson:likes`
	Matches   []string `json:matches bson:matches`
}

type UserMappingMultiple struct {
	Users UserMapping `json: "Users" bson: "Users"`
}

type APIResponse struct {
	StatusCode int `json: statusCode`
}

type UserMappingResp struct {
	Id        bson.ObjectId `json:"id" bson:"_id"`
	EMail     string        `json:email bson:email`
	Password  string        `json:password bson:password`
	FirstName string        `json:fName bson:fName`
	LastName  string        `json:lName bson:lName`
	Gender    string        `json:gender bson:gender`
	Class     string        `json:class bson:class`
	Hometown  string        `json:hometown bson:hometown`
	Major     string        `json:major bson:major`
	Smoke     bool          `json:smoke bson:smoke`
	Alcohol   bool          `json:alcohol bson:alcohol`
	Snore     bool          `json:snore bson:snore`
	Bio       string        `json:bio bson:bio`
	Bedtime   string        `json:bedtime bson:bedtime`
	Neatness  bool          `json:neatness bson:neatness`
	Likes     []string      `json:likes bson:likes`
	Matches   []string      `json:matches bson:matches`
}

type UsersMappingRespMultiple struct {
	Users []UserMappingResp `json:"Users" bson:"Users"`
}
