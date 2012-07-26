<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="11008008">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="classes" Type="Folder">
			<Property Name="NI.SortType" Type="Int">3</Property>
			<Item Name="main2.vi" Type="VI" URL="../classes/main2.vi"/>
			<Item Name="vehicleGeneric.lvclass" Type="LVClass" URL="../classes/genericVehicle/vehicleGeneric.lvclass"/>
			<Item Name="bike.lvclass" Type="LVClass" URL="../classes/bike/bike.lvclass"/>
			<Item Name="car.lvclass" Type="LVClass" URL="../classes/car/car.lvclass"/>
		</Item>
		<Item Name="classes2" Type="Folder">
			<Item Name="bus.lvclass" Type="LVClass" URL="../classes2/bus/bus.lvclass"/>
			<Item Name="genericVehicle.lvclass" Type="LVClass" URL="../classes2/genericVehicle.lvclass"/>
			<Item Name="main3.vi" Type="VI" URL="../classes2/generic/main3.vi"/>
			<Item Name="tricycle.lvclass" Type="LVClass" URL="../classes2/tricycle/tricycle.lvclass"/>
		</Item>
		<Item Name="clusters" Type="Folder">
			<Item Name="main.vi" Type="VI" URL="../clusters/main.vi"/>
			<Item Name="main_2.vi" Type="VI" URL="../clusters/main_2.vi"/>
			<Item Name="vehicleCluster.ctl" Type="VI" URL="../clusters/vehicleCluster.ctl"/>
		</Item>
		<Item Name="tricycle.ctl" Type="VI" URL="../classes2/tricycle/tricycle.ctl"/>
		<Item Name="vehicleCluster_2.ctl" Type="VI" URL="../clusters/vehicleCluster_2.ctl"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
