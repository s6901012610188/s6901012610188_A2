from datetime import datetime


# ==========================================
# คลาสสินค้า: เก็บข้อมูลของสินค้า 1 ชิ้น
# ==========================================
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def is_low_stock(self, limit=5):
        # สินค้าใกล้หมด ถ้าจำนวนคงเหลือน้อยกว่าหรือเท่ากับ limit
        return self.stock <= limit

    def show(self):
        print("[" + self.product_id + "] " + self.name
              + " | ราคา: " + str(self.price) + " บาท"
              + " | คงเหลือ: " + str(self.stock) + " ชิ้น")


# ==========================================
# คลาสคลังสินค้า: จัดการสินค้าทั้งหมด
# ==========================================
class Inventory:
    def __init__(self):
        self.products = []   # เก็บสินค้าทั้งหมด
        self.history = []    # เก็บประวัติการทำรายการ (เป็นข้อความ)

    # ---------- ฟังก์ชันช่วย ----------
    def add_history(self, text):
        # บันทึกประวัติพร้อมวันเวลา
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(now + " | " + text)

    def find_product(self, product_id):
        # ค้นหาสินค้าด้วยรหัส ถ้าไม่เจอจะคืนค่า None
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    # ---------- เพิ่ม / ลบ / แก้ไขสินค้า ----------
    def add_product(self, product_id, name, price, stock):
        if self.find_product(product_id) is not None:
            print("ผิดพลาด: รหัสสินค้านี้มีอยู่แล้ว")
            return

        if price < 0 or stock < 0:
            print("ผิดพลาด: ราคาและจำนวนต้องไม่ติดลบ")
            return

        new_product = Product(product_id, name, price, stock)
        self.products.append(new_product)
        self.add_history("เพิ่มสินค้า " + name + " จำนวน " + str(stock))
        print("เพิ่มสินค้าสำเร็จ: " + name)

    def remove_product(self, product_id):
        p = self.find_product(product_id)
        if p is None:
            print("ผิดพลาด: ไม่พบรหัสสินค้า " + product_id)
            return

        self.products.remove(p)
        self.add_history("ลบสินค้า " + p.name)
        print("ลบสินค้าสำเร็จ: " + p.name)

    def update_product(self, product_id, new_name, new_price):
        p = self.find_product(product_id)
        if p is None:
            print("ผิดพลาด: ไม่พบรหัสสินค้า " + product_id)
            return

        if new_price < 0:
            print("ผิดพลาด: ราคาต้องไม่ติดลบ")
            return

        p.name = new_name
        p.price = new_price
        self.add_history("แก้ไขสินค้า " + product_id + " เป็น " + new_name
                         + " ราคา " + str(new_price))
        print("แก้ไขสินค้าสำเร็จ")

    # ---------- แสดงสินค้า ----------
    def show_all(self):
        print("\n=== รายการสินค้าทั้งหมด ===")
        if len(self.products) == 0:
            print("ไม่มีสินค้าในคลัง")
        for p in self.products:
            p.show()

    # ---------- รับเข้า / ขายออก ----------
    def stock_in(self, product_id, amount):
        p = self.find_product(product_id)
        if p is None:
            print("ผิดพลาด: ไม่พบรหัสสินค้า " + product_id)
            return

        if amount <= 0:
            print("ผิดพลาด: จำนวนต้องมากกว่า 0")
            return

        p.stock = p.stock + amount
        self.add_history("รับเข้า " + p.name + " จำนวน " + str(amount))
        print("รับสินค้าเข้าสำเร็จ: " + p.name + " คงเหลือ " + str(p.stock) + " ชิ้น")

    def stock_out(self, product_id, amount):
        p = self.find_product(product_id)
        if p is None:
            print("ผิดพลาด: ไม่พบรหัสสินค้า " + product_id)
            return

        if amount <= 0:
            print("ผิดพลาด: จำนวนต้องมากกว่า 0")
            return

        if p.stock < amount:
            print("ผิดพลาด: สินค้าไม่พอ (มี " + str(p.stock) + " ชิ้น)")
            return

        p.stock = p.stock - amount
        total = p.price * amount
        self.add_history("ขาย " + p.name + " จำนวน " + str(amount)
                         + " รวม " + str(total) + " บาท")
        print("ขายสำเร็จ: " + p.name + " รวม " + str(total) + " บาท"
              + " (คงเหลือ " + str(p.stock) + " ชิ้น)")

    # ---------- รายงาน ----------
    def check_low_stock(self, limit=5):
        print("\n=== สินค้าใกล้หมด (คงเหลือ <= " + str(limit) + ") ===")
        found = False
        for p in self.products:
            if p.is_low_stock(limit):
                p.show()
                found = True
        if not found:
            print("ไม่มีสินค้าใกล้หมด")

    def show_history(self):
        print("\n=== ประวัติการทำรายการ ===")
        if len(self.history) == 0:
            print("ยังไม่มีประวัติ")
        for line in self.history:
            print(line)


# ==========================================
# ส่วนทดสอบโปรแกรม
# ==========================================
if __name__ == "__main__":
    inv = Inventory()

    # เพิ่มสินค้าเริ่มต้น
    inv.add_product("P01", "ปากกาน้ำเงิน", 15, 10)
    inv.add_product("P02", "สมุดโน้ต A5", 45, 3)
    inv.show_all()

    print("\n--- ทดสอบ 1: ขายสินค้า (สต็อกพอ) ---")
    inv.stock_out("P01", 2)

    print("\n--- ทดสอบ 2: ขายสินค้า (สต็อกไม่พอ) ---")
    inv.stock_out("P01", 15)

    print("\n--- ทดสอบ 3: ขายสินค้าที่ไม่มีในระบบ ---")
    inv.stock_out("P99", 1)

    print("\n--- ทดสอบ 4: เช็คสินค้าใกล้หมด ---")
    inv.check_low_stock(5)

    print("\n--- ทดสอบ 5: แก้ไขสินค้า ---")
    inv.update_product("P01", "ปากกาน้ำเงิน (ด้ามใหญ่)", 18)

    print("\n--- ทดสอบ 6: รับสินค้าเข้า ---")
    inv.stock_in("P02", 20)

    print("\n--- ทดสอบ 7: ลบสินค้า ---")
    inv.add_product("P03", "ยางลบ", 5, 100)
    inv.remove_product("P03")
    inv.remove_product("P03")   # ลบซ้ำ ต้องแจ้งว่าไม่พบ

    inv.show_all()
    inv.show_history()