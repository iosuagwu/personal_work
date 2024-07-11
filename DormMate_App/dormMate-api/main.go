package main

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/Masterminds/semver"
	"github.com/gorilla/mux"
	"github.com/rs/cors"

	"goProjects/sp-gia/dormMate-api/handlers"
)

const (
	version string = "v0.0.0"
)

type Route struct {
	Name        string
	Method      string
	Pattern     string
	HandlerFunc http.HandlerFunc
}

type Routes []Route

func createRoutes(DM *handlers.DormMateAPI) Routes {
	v := semver.MustParse(version)
	routePrefix := "/v" + strconv.FormatInt(v.Major(), 10)

	return Routes{
		Route{
			"Root",
			"GET",
			routePrefix,
			DM.Root,
		},

		Route{
			"CreateNewUser",
			"POST",
			routePrefix + "/newUser",
			DM.CreateNewUser,
		},

		Route{
			"UpdateUser",
			"PUT",
			routePrefix + "/updateUser",
			DM.UpdateUser,
		},

		Route{
			"GetSingleUser",
			"GET",
			routePrefix + "/singleUser",
			DM.GetSingleUser,
		},

		Route{
			"GetAllUsers",
			"GET",
			routePrefix + "/allUsers",
			DM.GetAllUsers,
		},
	}
}

func NewDormMateRouter(routes Routes) *mux.Router {
	router := mux.NewRouter().StrictSlash(true)

	for _, route := range routes {
		router.
			Methods(route.Method).
			Path(route.Pattern).
			Name(route.Name).
			Handler(route.HandlerFunc)
	}
	return router
}

func main() {

	DormMate := handlers.NewDormMateAPI()
	routes := createRoutes(DormMate)
	router := NewDormMateRouter(routes)
	handler := cors.AllowAll().Handler(router)
	fmt.Println(http.ListenAndServe("0.0.0.0:8080", handler))
}
