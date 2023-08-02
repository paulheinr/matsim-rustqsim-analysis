package org.matsim.analysis;

import org.matsim.api.core.v01.population.Population;
import org.matsim.core.population.PopulationUtils;

public class BerlinPlansCleaner {
    public static void main(String[] args) {
        Population population = PopulationUtils.readPopulation("C:\\Users\\Paul Heinrich\\Downloads\\berlin-without-pt\\berlin-without-pt\\berlin-10pct-all-plans-no-pt.xml.gz");

        System.out.println("Persons before: " + population.getPersons().size());

//        Map<Id<Person>, ? extends Person> persons = population.getPersons();
//        for (Person person : persons.values()) {
//            for (Plan plan : person.getPlans()) {
//                plan.getPlanElements()
//                        .removeIf(element -> element instanceof Leg ||
//                                (element instanceof Activity && ((Activity) element).getType().equals("car interaction")) ||
//                                (element instanceof Activity && ((Activity) element).getType().equals("ride interaction")) ||
//                                (element instanceof Activity && ((Activity) element).getType().contains("freight")));
//            }
//
//        }

        population.getPersons().entrySet().removeIf(p -> p.getKey().toString().contains("freight"));

        System.out.println("Persons after: " + population.getPersons().size());

        PopulationUtils.writePopulation(population, "C:\\Users\\Paul Heinrich\\Downloads\\berlin-without-pt\\berlin-without-pt\\berlin-10pct-all-plans-no-pt-no-freight.xml.gz");
//        Population population = PopulationUtils.readPopulation("C:\\Users\\Paul Heinrich\\Downloads\\berlin-without-pt\\berlin-without-pt\\berlin-10pct-all-plans-no-pt-clean-no-freight.xml.gz");
//        int popSize = population.getPersons().size();
//        System.out.println("Population size: " + popSize);
//
//        long activities = population.getPersons().values().stream().flatMap(p -> p.getPlans().stream()).mapToLong(p -> p.getPlanElements().size()).sum();
//        System.out.println("Activities per agent: " + (double) activities / popSize);
    }
}
