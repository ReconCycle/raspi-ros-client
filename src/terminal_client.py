#! /usr/bin/env python
import rospy
import rosservice
from digital_interface_msgs.srv import ConfigRead, ConfigSet,ConfigSetRequest


class MinimalClientAsync(object):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self):
        self.req.a = int(sys.argv[1])
        self.req.b = int(sys.argv[2])
        self.future = self.cli.call_async(self.req)



def main(args=None):


    #rospy.create_client()
    #rospy.create_client()
  

    #get all services
    service_list=rosservice.get_service_list()

    #search for the configuration services
    raspi_services=[]
    for i in service_list:
        if 'config_set_new' in i:
            raspi_services.append(i)

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
        read_proxy= rospy.ServiceProxy('config_read_current', ConfigRead)

    elif chosen_template==2:
        print('Empty template it is.')
        read_proxy= rospy.ServiceProxy('config_read_template', ConfigRead)

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

        template_msg.pin_configs[pin_number-1].service_name=str(raw_input('Write desired service name:'))

        pin_number=int(input('Which pin you want to configure next? (write number pin or write 0 if you are finish):'))


    
    print('Sending config')
    write_proxy= rospy.ServiceProxy('config_set_new', ConfigSet)

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

