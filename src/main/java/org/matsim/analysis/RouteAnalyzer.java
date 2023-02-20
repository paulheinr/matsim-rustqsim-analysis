package org.matsim.analysis;

import org.apache.commons.lang.builder.EqualsBuilder;
import org.apache.commons.lang.builder.HashCodeBuilder;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.events.LinkLeaveEvent;
import org.matsim.api.core.v01.events.PersonEntersVehicleEvent;
import org.matsim.api.core.v01.events.PersonLeavesVehicleEvent;
import org.matsim.api.core.v01.events.handler.LinkLeaveEventHandler;
import org.matsim.api.core.v01.events.handler.PersonEntersVehicleEventHandler;
import org.matsim.api.core.v01.events.handler.PersonLeavesVehicleEventHandler;
import org.matsim.api.core.v01.network.Link;
import org.matsim.api.core.v01.population.Person;
import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.events.EventsUtils;
import org.matsim.vehicles.Vehicle;

import java.io.IOException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class RouteAnalyzer implements PersonEntersVehicleEventHandler, PersonLeavesVehicleEventHandler, LinkLeaveEventHandler {
    private final List<Route> routes = new LinkedList<>();
    private final List<Route> cachedUnfinishedRoutes = new LinkedList<>();
    private final Map<Id<Vehicle>, Id<Person>> personInVehicle = new HashMap<>();

    public static void main(String[] args) throws IOException {
        String pathToEventsFile = "./results/output_events.xml";

        EventsManager manager = EventsUtils.createEventsManager();
        RouteAnalyzer handler = new RouteAnalyzer();
        manager.addHandler(handler);
        EventsUtils.readEvents(manager, pathToEventsFile);
        handler.printResult();
        handler.exportResult();
    }

    @Override
    public void handleEvent(PersonEntersVehicleEvent personEntersVehicleEvent) {
        Id<Person> personId = personEntersVehicleEvent.getPersonId();

        assert cachedUnfinishedRoutes.stream().noneMatch(route -> route.personId == personId);
        cachedUnfinishedRoutes.add(new Route(personId));
        personInVehicle.put(personEntersVehicleEvent.getVehicleId(), personId);
    }

    @Override
    public void handleEvent(PersonLeavesVehicleEvent personLeavesVehicleEvent) {
        Route cachedRoute = getCachedRoute(personLeavesVehicleEvent.getVehicleId());
        assert cachedRoute.getTravelledLinks().size() + 1 == cachedRoute.getTravelTimes().size() : "Cached Route is corrupted.";
        routes.add(cachedRoute);
        cachedUnfinishedRoutes.remove(cachedRoute);

        personInVehicle.remove(personLeavesVehicleEvent.getPersonId());
    }

    @Override
    public void handleEvent(LinkLeaveEvent linkLeaveEvent) {
        Route cachedRoute = this.getCachedRoute(linkLeaveEvent.getVehicleId());
        if (cachedRoute.getTravelTimes().isEmpty()) {
            // This link is where a PersonEntersVehicleEvent happened, thus it was not travelled fully.
            // add begin travel time
            cachedRoute.addTravelTime(linkLeaveEvent.getTime());
            return;
        }
        cachedRoute.addTravelledLink(linkLeaveEvent.getLinkId()).addTravelTime(linkLeaveEvent.getTime());
    }

    private Route getCachedRoute(Id<Vehicle> vehicleId) {
        Id<Person> personId = this.personInVehicle.get(vehicleId);
        assert personId != null;
        List<Route> routes = this.cachedUnfinishedRoutes.stream().filter(route -> route.personId == personId).toList();
        assert routes.size() == 1;
        return routes.get(0);
    }

    public List<Route> getRoutes() {
        return this.routes;
    }

    private void exportResult() {
    }

    private void printResult() {
        for (Route route : this.routes) {
            System.out.println("----- Route -----");
            System.out.println(route);
        }
    }

    public static class Route {
        private final Id<Person> personId;
        private final List<Id<Link>> travelledLinks = new LinkedList<>();
        private final List<Double> travelTimes = new LinkedList<>();

        public Route(Id<Person> personId) {
            this.personId = personId;
        }

        public void addTravelTime(double travelTime) {
            this.travelTimes.add(travelTime);
        }

        public Route addTravelledLink(Id<Link> link) {
            this.travelledLinks.add(link);
            return this;
        }

        public List<Id<Link>> getTravelledLinks() {
            return travelledLinks;
        }

        public List<Double> getTravelTimes() {
            return travelTimes;
        }

        public Id<Person> getId() {
            return personId;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;

            if (o == null || getClass() != o.getClass()) return false;

            Route route = (Route) o;

            return new EqualsBuilder().append(personId, route.personId).append(travelledLinks, route.travelledLinks).append(travelTimes, route.travelTimes).isEquals();
        }

        @Override
        public int hashCode() {
            return new HashCodeBuilder(17, 37).append(personId).append(travelledLinks).append(travelTimes).toHashCode();
        }

        @Override
        public String toString() {
            return "Route{" +
                    "id=" + personId +
                    ", travelledLinks=" + travelledLinks +
                    ", travelTimes=" + travelTimes +
                    '}';
        }
    }
}
