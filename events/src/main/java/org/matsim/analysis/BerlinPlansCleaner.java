package org.matsim.analysis;

import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.population.*;
import org.matsim.core.population.PopulationUtils;

import java.util.Map;

public class BerlinPlansCleaner {
    public static void main(String[] args) {
        Population population = PopulationUtils.readPopulation("C:\\Users\\Paul Heinrich\\Downloads\\berlin-without-pt\\berlin-without-pt\\berlin-10pct-all-plans-no-pt.xml.gz");

        Map<Id<Person>, ? extends Person> persons = population.getPersons();
        for (Person person : persons.values()) {
            for (Plan plan : person.getPlans()) {
                plan.getPlanElements()
                        .removeIf(element -> element instanceof Leg ||
                                (element instanceof Activity && ((Activity) element).getType().equals("car interaction")) ||
                                (element instanceof Activity && ((Activity) element).getType().equals("ride interaction")) ||
                                (element instanceof Activity && ((Activity) element).getType().contains("freight")));
            }

        }

        population.getPersons().entrySet().removeIf(p -> p.getKey().toString().contains("freight"));

        PopulationUtils.writePopulation(population, "C:\\Users\\Paul Heinrich\\Downloads\\berlin-without-pt\\berlin-without-pt\\berlin-10pct-all-plans-no-pt-clean-no-freight.xml.gz");
    }
}
