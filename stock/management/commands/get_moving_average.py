from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from stock.models import Company
from stock.views import calculate_moving_average

class Command(BaseCommand):
    help = 'Calculates moving averages for a specified date range and period'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start_date', required=False, type=str, help='Start date (YYYY-MM-DD)')
        parser.add_argument('-e', '--end_date', required=False, type=str, help='End date (YYYY-MM-DD)')
        parser.add_argument('-p', '--period', required=False, type=int, help='Period for the moving average')

    def handle(self, *args, **options):
        start_date = options['start_date']
        end_date = options['end_date']
        period = options['period']

        if not period:
            raise CommandError('Missing required arguments: start_date, end_date, or period')

        # Convert string dates to datetime objects
        if not start_date or not end_date:
            start_date = datetime.today()
            end_date = datetime.today()
        else:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError as e:
                raise CommandError('Invalid date format. Please use YYYY-MM-DD.')

        # Assuming you want to calculate moving averages for all companies
        # Adjust logic here if you need to target specific companies
        companies = Company.objects.all()

        for company in companies:
            # Proxy function to calculate moving averages
            # You may need to adjust this function to support date ranges and multiple companies
            
            current_date = start_date
            while current_date <= end_date:
                result = calculate_moving_average(company, reference_date=current_date, period=period)
                current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(f'Successfully calculated moving average'))
