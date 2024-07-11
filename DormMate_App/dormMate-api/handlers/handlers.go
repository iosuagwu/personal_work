package handlers

import (
	"encoding/json"
	"fmt"
	"goProjects/sp-gia/dormMate-api/db"
	. "goProjects/sp-gia/dormMate-api/models"
	"net/http"

	"github.com/gorilla/mux"
)

const DOMAIN = "dormmate.com"

type DormMateAPI struct {
	myConnection *db.MongoConnection
}

type JSONstring string

func (j JSONstring) MarshalJSON() ([]byte, error) {
	return []byte(j), nil
}

func NewDormMateAPI() *DormMateAPI {
	DM := &DormMateAPI{
		myConnection: db.NewDBConnection(),
	}
	return DM
}

func (Dm *DormMateAPI) Root(w http.ResponseWriter, r *http.Request) {
	welcome := `{
					"welcome" : "we have lift off."
				}`
	content, _ := json.Marshal(JSONstring(welcome))
	fmt.Fprintf(w, "%s", string(content))
}

func (Dm *DormMateAPI) CreateNewUser(w http.ResponseWriter, r *http.Request) {
	reqBodyStruct := new(UserMapping)
	responseEncoder := json.NewEncoder(w)
	if err := json.NewDecoder(r.Body).Decode(&reqBodyStruct); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		if err := responseEncoder.Encode(&APIResponse{StatusCode: http.StatusBadRequest}); err != nil {
			fmt.Fprintf(w, "Error occurred while processing POST request %v \n", err.Error())
		}
		return
	}

	err := Dm.myConnection.AddUser(reqBodyStruct.ID, reqBodyStruct.EMail, reqBodyStruct.Password)

	if err != nil {
		w.WriteHeader(http.StatusConflict)
		if err := responseEncoder.Encode(&APIResponse{StatusCode: http.StatusBadRequest}); err != nil {
			fmt.Fprintf(w, "Error %s occured while trying to add user \n", err.Error())
		}
	}
	responseEncoder.Encode(&APIResponse{StatusCode: http.StatusOK})
}

func (Dm *DormMateAPI) UpdateUser(w http.ResponseWriter, r *http.Request) {
	//err := Dm.myConnection.UpdateUser()

	return
}

func (Dm *DormMateAPI) GetSingleUser(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	email := vars["email"]

	//singleUser := Dm.myConnection.GetSingleUser(email)

	//content, _ := json.Marshal(singleUser)
	fmt.Fprintf(w, "%s \n", email)

	return
}

func (Dm *DormMateAPI) GetAllUsers(w http.ResponseWriter, r *http.Request) {
	allUsers := Dm.myConnection.GetAllUsers()

	var response UsersMappingRespMultiple
	response.Users = allUsers

	content, _ := json.Marshal(response)
	fmt.Fprintf(w, "%s \n", string(content))

	return
}
