import random
import json
import argparse
import math
from typing import Dict, Any, Tuple

class ProductionSimulator:
    def __init__(self, products: Dict[str, Dict[str, Any]], overall_daily_capacity: int):
        """
        :param products: mapping of product name to its parameters:
            - unit_time (float): minutes per unit
            - daily_capacity (int): max units/day per product
            - quantity (int): units to produce
        :param overall_daily_capacity: max total units/day for all products
        """
        self.products = products
        self.overall_daily_capacity = overall_daily_capacity

    @staticmethod
    def generate_random_quantities(product_names, min_qty=50, max_qty=200) -> Dict[str, int]:
        return {name: random.randint(min_qty, max_qty) for name in product_names}

    @staticmethod
    def generate_random_parameters(product_names) -> Tuple[Dict[str, Dict[str, Any]], int]:
        params = {}
        for name in product_names:
            params[name] = {
                'unit_time': round(random.uniform(0.5, 2.0), 2),  # minutes per unit
                'daily_capacity': random.randint(100, 500)        # units per day
            }
        overall_capacity = random.randint(1000, 2000)
        return params, overall_capacity

    def calculate_total_time(self) -> Tuple[float, float]:
        total_minutes = sum(
            specs['quantity'] * specs['unit_time']
            for specs in self.products.values()
        )
        total_hours = round(total_minutes / 60, 2)

        if self.overall_daily_capacity <= 0:
            total_days = math.inf
        else:
            max_unit_time = max(specs['unit_time'] for specs in self.products.values())
            daily_max_minutes = self.overall_daily_capacity * max_unit_time
            total_days = round(total_minutes / daily_max_minutes, 2) if daily_max_minutes > 0 else math.inf

        return total_hours, total_days

    def report(self) -> str:
        lines = ["--- Production Simulation Report ---"]
        lines.append("Products configuration:")
        for name, specs in self.products.items():
            lines.append(
                f"{name}: quantity={specs['quantity']} units, unit_time={specs['unit_time']} min, "
                f"daily_capacity={specs['daily_capacity']} units/day"
            )
        lines.append(f"Overall daily capacity: {self.overall_daily_capacity} units/day")

        total_hours, total_days = self.calculate_total_time()
        lines.append(f"Total production time: {total_hours} hours (~{total_days} days)")
        return "\n".join(lines)


def load_manual_config(path: str) -> Tuple[Dict[str, Dict[str, Any]], int]:
    with open(path, 'r') as f:
        data = json.load(f)
    return data['products'], data['overall_daily_capacity']


def main():
    parser = argparse.ArgumentParser(description="Production Simulator")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--auto', action='store_true', help='Use random configuration')
    group.add_argument('--config', type=str, help='Path to manual JSON config file')
    args = parser.parse_args()

    # Default product names
    product_names = ['Product 1', 'Product 2', 'Product 3', 'Product 4', 'Product 5', 'Product 6']

    if args.config:
        products_config, overall_capacity = load_manual_config(args.config)
    else:
        quantities = ProductionSimulator.generate_random_quantities(product_names)
        params, overall_capacity = ProductionSimulator.generate_random_parameters(product_names)
        products_config = {
            name: {
                'quantity': quantities[name],
                'unit_time': params[name]['unit_time'],
                'daily_capacity': params[name]['daily_capacity']
            } for name in product_names
        }

    simulator = ProductionSimulator(products_config, overall_capacity)

    # Print report and export
    print(simulator.report())
    output = {
        'products': products_config,
        'overall_daily_capacity': overall_capacity,
        'total_hours': simulator.calculate_total_time()[0],
        'total_days': simulator.calculate_total_time()[1]
    }
    with open('simulation_output.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("\nSimulation data exported to simulation_output.json")

if __name__ == '__main__':
    main()
