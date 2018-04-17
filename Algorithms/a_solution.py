def a_solution(station_list):
    """Finds a set of connections"""
    #print(random_int)
    #print(station_list[random_int].name)
    # zoek naam stations connections
    # pak de eerste die je tegen komt
    # Einde traject
    end_time = 0
    for station in station_list:
        attempt = sn.Solution
        for connection in connections:
            if connection.begin == station.name or connection.end == station.name:
                print(connection.begin)
                route = [connection.begin, connection.end]
                duration = connection.time
                route = rt.Route(route)
                print(route.time)
                end_time += int(duration)
                attempt.append(route, end_time)
                print(end_time)

                break
