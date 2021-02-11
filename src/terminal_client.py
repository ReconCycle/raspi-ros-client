#! /usr/bin/env python
import rospy
import rosservice
from digital_interface_msgs.srv import ConfigRead, ConfigSet,ConfigSetRequest
import os.path



def main(args=None):

    #rospy.create_client()
    #rospy.create_client()
  

    #get all services
    service_list=rosservice.get_service_list()

    #search for the configuration services
    raspi_services=[]
    for i in service_list:
        if 'config_set_new' in i:
            i = i.replace('config_set_new','')
            raspi_services.append(i)

    if len(raspi_services)==0:
        print('Hello! I\'m Rassberry ROS configuration client. No Raspberries services in my reach!')
        return

    else:    
        print('Hello! I\'m Rassberry ROS configuration client. I have next Raspberries in my reach:')

    j=0
    for i in raspi_services:
        j=j+1
        print(str(j)+'.  '+str(i))


    chosen_raspi=int(input('Choose number of the one that you want to configure:'))
    print('You have choosen: ' + str(chosen_raspi))




    chosen_template=int((raw_input('Configure from now active configuration (write 1) or empty template (write 2)? (default = 1)')) or 1)
    
    if chosen_template==1:
        print('Active configuration it is.')
        demand_name=raspi_services[chosen_raspi-1]+'config_read_current'
        #read_proxy= rospy.ServiceProxy('config_read_current', ConfigRead)

    elif chosen_template==2:
        print('Empty template it is.')
        demand_name=raspi_services[chosen_raspi-1]+'config_read_template'
        #read_proxy= rospy.ServiceProxy('config_read_template', ConfigRead)

    read_proxy= rospy.ServiceProxy(demand_name, ConfigRead)

    template_msg = read_proxy().config

    print(template_msg)

    pin_number=int(input('Which pin you want to configure? (write number pin or write 0 if you are finish):'))




    while (pin_number!=0):
        print('Current pin configuration:')
        print(template_msg.pin_configs[pin_number-1])
        
        wrong_config=True
        while wrong_config:
            chosen_pin_config=str(raw_input('Write desired configuration:'))
       

            if chosen_pin_config in template_msg.pin_configs[pin_number-1].available_config:

                template_msg.pin_configs[pin_number-1].actual_config=chosen_pin_config
                wrong_config=False

            else:
                print('wrong config, try again with this!')
                print(template_msg.pin_configs[pin_number-1].available_config)




        if chosen_pin_config=='empty':

            template_msg.pin_configs[pin_number-1].service_name=''
        else:



            print('Setting parameters (write parameter name END to finish)')
            parameter_name='General'
            template_msg.pin_configs[pin_number-1].config_parameters=[]
            parameter_name=str(raw_input('Parameter name:'))
            while parameter_name!='END':        
                parameter_value=str(raw_input('Parameter value:'))
                template_msg.pin_configs[pin_number-1].config_parameters.append(parameter_name)
                template_msg.pin_configs[pin_number-1].config_parameters.append(parameter_value)
                parameter_name=str(raw_input('Parameter name:'))



            template_msg.pin_configs[pin_number-1].service_name=str(raw_input('Write desired service name:'))

        pin_number=int(input('Which pin you want to configure next? (write number pin or write 0 if you are finish):'))


    
    print('Sending config')
    write_proxy= rospy.ServiceProxy(raspi_services[chosen_raspi-1]+'config_set_new', ConfigSet)

    response = write_proxy(template_msg)
      


    if False:
        rclpy.init(args=args)

        minimal_client = MinimalClientAsync()
        minimal_client.send_request()

        while rclpy.ok():
            rclpy.spin_once(minimal_client)
            if minimal_client.future.done():
                try:
                    response = minimal_client.future.result()
                except Exception as e:
                    minimal_client.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    minimal_client.get_logger().info(
                        'Result of add_two_ints: for %d + %d = %d' %
                        (minimal_client.req.a, minimal_client.req.b, response.sum))
                break




if __name__ == '__main__':
    main()

