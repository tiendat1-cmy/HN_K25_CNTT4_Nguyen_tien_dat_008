import tabulate

class Vehicle:
    def __init__(self, vehicle_id, vehicle_name, license_plate,base_maintenance_fee, kilometers, cost_per_km):
        self.id = vehicle_id
        self.vehicle_name = vehicle_name
        self.license_plate = license_plate
        self.base_maintenance_fee = base_maintenance_fee
        self.kilometers = kilometers
        self.cost_per_km = cost_per_km

        self.total_maintenance_cost = 0
        self.maintenance_type = ""

        self.calculate_maintenance_cost()
        self.classify_maintenance()

    def calculate_maintenance_cost(self):
        self.total_maintenance_cost = (self.base_maintenance_fee+ self.kilometers * self.cost_per_km)

    def classify_maintenance(self):
        if self.total_maintenance_cost < 1_000_000:
            self.maintenance_type = "Thấp"
        elif self.total_maintenance_cost < 5_000_000:
            self.maintenance_type = "Trung bình"
        elif self.total_maintenance_cost < 15_000_000:
            self.maintenance_type = "Cao"
        else:
            self.maintenance_type = "Rất cao"


class VehicleManager:
    def __init__(self):
        self.vehicles = []

    def input_positive_number(self, message):
        while True:
            try:
                value = float(input(message))
                if value < 0:
                    print("Giá trị phải lớn hơn hoặc bằng 0!")
                    continue
                return value
            except ValueError:
                print("Vui lòng nhập số hợp lệ!")
    # check trùng id
    def find_by_id(self, vehicle_id):
        for vehicle in self.vehicles:
            if vehicle.id == vehicle_id:
                return vehicle
        return None
    # check biển số xe
    def find_by_license_plate(self, license_plate):
        for vehicle in self.vehicles:
            if vehicle.license_plate.lower() == license_plate.lower():
                return vehicle
        return None
    # thêm phương tiện
    def add_vehicle(self):
        print("\n --- THÊM PHƯƠNG TIỆN ---")

        while True:
            vehicle_id = input("Nhập mã phương tiện: ").strip().upper()
            if not vehicle_id:
                print("Mã phương tiện không được rỗng!")
                continue
            if self.find_by_id(vehicle_id):
                print("Mã phương tiện đã tồn tại!")
                continue
            break

        while True:
            vehicle_name = input("Nhập tên phương tiện: ").strip()
            if not vehicle_name:
                print("Tên phương tiện không được rỗng!")
                continue
            break

        while True:
            license_plate = input("Nhập biển số xe: ").strip()
            if not license_plate:
                print("Biển số xe không được rỗng!")
                continue
            if self.find_by_license_plate(license_plate):
                print("Biển số xe đã tồn tại!")
                continue
            break

        base_maintenance_fee = self.input_positive_number("Nhập phí bảo trì cố định: ")
        kilometers = self.input_positive_number("Nhập số km đã đi: ")
        cost_per_km = self.input_positive_number("Nhập chi phí bảo trì mỗi km: ")

        vehicle = Vehicle(vehicle_id, vehicle_name, license_plate,base_maintenance_fee, kilometers, cost_per_km)
        self.vehicles.append(vehicle)
        print("Thêm phương tiện thành công!")

    # hiển thị danh sách
    def show_all(self):
        if not self.vehicles:
            print("Danh sách phương tiện đang rỗng!")
            return

        table_data = []
        for vehicle in self.vehicles:
            table_data.append([
                vehicle.id,
                vehicle.vehicle_name,
                vehicle.license_plate,
                f"{vehicle.base_maintenance_fee:,.0f}",
                f"{vehicle.kilometers:,.0f}",
                f"{vehicle.cost_per_km:,.0f}",
                f"{vehicle.total_maintenance_cost:,.0f}",
                vehicle.maintenance_type
            ])

        print(tabulate.tabulate(
            table_data,
            headers=["Mã PT", "Tên phương tiện", "Biển số","Phí cố định", "Km đã đi", "Chi phí/km","Tổng bảo trì", "Phân loại"],
            tablefmt="grid"))
        
    # cập nhật phương tiện
    def update_vehicle(self):
        vehicle_id = input("Nhập mã phương tiện cần cập nhật: ").strip().upper()
        vehicle = self.find_by_id(vehicle_id)

        if not vehicle:
            print("Không tìm thấy phương tiện cần cập nhật!")
            return

        vehicle.base_maintenance_fee = self.input_positive_number("Nhập phí bảo trì cố định mới: ")
        vehicle.kilometers = self.input_positive_number("Nhập số km mới: ")
        vehicle.cost_per_km = self.input_positive_number("Nhập chi phí/km mới: ")

        vehicle.calculate_maintenance_cost()
        vehicle.classify_maintenance()
        print("Cập nhật phương tiện thành công!")
    
    # xóa phương tiện
    def delete_vehicle(self):
        vehicle_id = input("Nhập mã phương tiện cần xóa: ").strip().upper()
        vehicle = self.find_by_id(vehicle_id)
        if not vehicle:
            print("Không tìm thấy phương tiện cần xóa!")
            return
        confirm = input("Bạn có chắc muốn xóa phương tiện này không? (Y/N): ").strip().lower()
        if confirm == "y":
            self.vehicles.remove(vehicle)
            print("Xóa phương tiện thành công!")
        elif confirm == "n":
            print("Đã hủy thao tác xóa!")
        else:
            print("Lựa chọn không hợp lệ!")
    # tìm kiếm 
    def search_vehicle(self):
        keyword = input("Nhập từ khóa tìm kiếm: ").strip().lower()
        results = [
            v for v in self.vehicles
            if keyword in v.vehicle_name.lower()or keyword in v.license_plate.lower()]

        if not results:
            print("Không tìm thấy phương tiện phù hợp!")
            return

        table_data = [[v.id, v.vehicle_name, v.license_plate,f"{v.total_maintenance_cost:,.0f}", v.maintenance_type] for v in results]

        print(tabulate.tabulate(
            table_data,
            headers=["Mã PT", "Tên phương tiện", "Biển số","Tổng bảo trì", "Phân loại"],
            tablefmt="grid"))

def main():
    manager = VehicleManager()
    while True:
        
        choice = input("""================ MENU ================
1. Hiển thị danh sách phương tiện
2. Thêm phương tiện mới
3. Cập nhật phương tiện
4. Xóa phương tiện
5. Tìm kiếm phương tiện
6. Thoát
=====================================
Nhập lựa chọn của bạn:""")

        match choice:
            case "1":
                manager.show_all()
            case "2":
                manager.add_vehicle()
            case "3":
                manager.update_vehicle()
            case "4":
                manager.delete_vehicle()
            case "5":
                manager.search_vehicle()
            case "6":
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý phương tiện!")
                break
            case _:
                print("Vui lòng nhập từ 1 đến 6!")


if __name__ == "__main__":
    main()