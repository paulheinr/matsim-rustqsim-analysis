package org.matsim.analysis;

import it.geosolutions.jaiext.jts.CoordinateSequence2D;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.LinearRing;
import org.locationtech.jts.geom.Polygon;

public class JtsPlayground {
    public static void main(String[] args) {
        GeometryFactory factory = new GeometryFactory();
        Polygon square = new Polygon(new LinearRing(new CoordinateSequence2D(0, 0, 0, 1, 1, 1, 1, 0, 0, 0), factory), null, factory);
        Polygon sandClock = new Polygon(new LinearRing(new CoordinateSequence2D(0, 0, 0, 1, 1, 0, 1, 1, 0, 0), factory), null, factory);
        System.out.println("Square area: " + square.getArea());
        System.out.println("Sand-clock area: " + sandClock.getArea());
    }
}
