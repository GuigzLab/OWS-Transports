from flask import Flask
from flask import render_template
from flask import request
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Parse an RDF file in Turtle format
g = Graph()
g.parse("models/transports.ttl", format="turtle")


def exec_query(graph, query):
    results = graph.query(query)
    headers = [str(v) for v in results.vars]
    cleaned_res = []
    # Affichage des résultats de la requête
    for row in results:
        r = []
        for x in row:
            r.append(str(x))
        cleaned_res.append(r)

    return headers, cleaned_res


app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html', name="main page")


@app.route("/locations")
def locations(title=None):

    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX : <http://www.ows.fr/pariscite/ontologies/transports#>

        SELECT ?Location ?Type ?Name
        WHERE {
            ?Location a ?Type; :locationName ?Name.
            ?Type rdfs:subClassOf* :Location.
        }
    """
    h, r = exec_query(graph=g, query=query)

    return render_template('index.html', title="Liste des lieux", headers=h, results=r)


@app.route("/persons")
def persons(title=None):

    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX : <http://www.ows.fr/pariscite/ontologies/transports#>

        SELECT ?Person ?Type ?PersonID ?BirthName
        WHERE {
            ?Person a ?Type; :birthName ?BirthName; :personId ?PersonID.
            ?Type rdfs:subClassOf* :Person.
        }
    """
    h, r = exec_query(graph=g, query=query)

    return render_template('index.html', title="Liste des personnes", headers=h, results=r)


@app.route("/vehicles")
def vehicles(title=None):

    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX : <http://www.ows.fr/pariscite/ontologies/transports#>

        SELECT ?Vehicle ?Type ?Name ?LicencePlate ?CO2
        WHERE {
            ?Vehicle a ?Type; :vehicleModel ?Name; :licencePlate ?LicencePlate; :carbonEmissions ?CO2.
            ?Type rdfs:subClassOf* :Vehicle.
        }
    """
    h, r = exec_query(graph=g, query=query)

    return render_template('index.html', title="Liste des véhicules", headers=h, results=r)


@app.route("/trips")
def trips(title=None):

    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX : <http://www.ows.fr/pariscite/ontologies/transports#>

        SELECT ?trip (group_concat(distinct ?name;separator="; ") as ?names) ?startLocation ?endLocation (group_concat(distinct ?model;separator="; ") as ?models) (concat(str(?startTime), " to ", str(?endTime)) as ?timeRange)
        WHERE {
            ?trip a :Trip; :hasPassenger ?passenger; :uses ?vehicle; :startFrom ?startLocation; :endAt ?endLocation; :startTime ?startTime; :endTime ?endTime.
            ?vehicle :vehicleModel ?model.
            ?passenger :birthName ?name.
        }
        GROUP BY ?trip ?startLocation ?endLocation ?startTime ?endTime
    """
    h, r = exec_query(graph=g, query=query)

    return render_template('index.html', title="Liste des trajets", headers=h, results=r)


@app.route("/uri/<value>")
def uri(value):

    # value = request.args.get("value")

    # if value == None:
    #     # TODO : 404
    #     return render_template('index.html', title="Ressource non trouvée")

    full_uri = f"<http://www.ows.fr/pariscite/ontologies/transports#{value}>"
    print(full_uri)

    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX transports: <http://www.ows.fr/pariscite/ontologies/transports#>

        SELECT ?Predicate ?Object
        WHERE {
        {
            URI_TO_REPLACE ?Predicate ?Object .
        }
        UNION
        {
            ?Object ?Predicate URI_TO_REPLACE .
        }
        }
    """

    query = query.replace('URI_TO_REPLACE', full_uri)

    h, r = exec_query(graph=g, query=query)

    return render_template('index.html', title=f"Description de {value}", headers=h, results=r)


@app.route('/search')
def search():
    search = request.args.get('q')
    if not search:
        return render_template('search.html', title=f"Recherche", display=False)

    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?Resource ?Predicate ?Object
        WHERE {
        ?Resource ?Predicate ?Object .
        FILTER(regex(?Object, "TO_REPLACE", "i") || 
                regex(str(?Resource), "TO_REPLACE", "i") || 
                regex(str(?Predicate), "TO_REPLACE", "i") || 
                regex(xsd:string(?Object), "TO_REPLACE", "i"))
        }
    """

    query = query.replace('TO_REPLACE', search)
    print(search)
    h, r = exec_query(graph=g, query=query)

    resource_url = "http://dbpedia.org/resource/" + search
    g_dbp = Graph()
    g_dbp.parse(resource_url)

    query = prepareQuery(
        """
        SELECT *
        WHERE {
            ?Resource ?Predicate ?Object .
            FILTER(?Resource = <""" + resource_url + """>)
        }
        """
    )

    dbp_h, dbp_r = exec_query(graph=g_dbp, query=query)

    return render_template('search.html', title=f"Recherche", display=True, headers=h, results=r, dbp_headers=dbp_h, dbp_results=dbp_r)


@app.route('/dbpedia')
def dbpedia():
    search = request.args.get('q')
    if not search:
        return render_template('search.html', title=f"Recherche", display=False)

    g_dbp = Graph()
    resource_url = "http://dbpedia.org/resource/" + search

    g_dbp.parse(resource_url)

    query = prepareQuery(
        """
        SELECT *
        WHERE {
            <""" + resource_url + """> ?Predicate ?Object .
        }
        """
    )

    h, r = exec_query(graph=g_dbp, query=query)

    return render_template('search.html', title=f"Recherche", display=True, headers=h, results=r)
